"""Extract structured facts from issues using Gemini."""

import argparse
import json
import re
import sys
import time

import httpx

from config import EXTRACTED_DIR, GEMINI_API_BASE, GEMINI_API_KEY, GEMINI_MODEL, HUBEAU_APIS, RAW_DATA_DIR

EXTRACTION_PROMPT = """\
Tu es un expert en hydrologie et en APIs de données environnementales. Tu analyses des issues GitHub du projet Hub'Eau (plateforme d'accès aux données sur l'eau en France).

Analyse l'issue suivante et extrais les faits utiles. Ignore le bruit (remerciements, demandes de statut, etc.).

## Issue #{number}: {title}

**État:** {state} | **Labels:** {labels} | **Date:** {created_at}

### Contenu
{body}

### Commentaires
{comments}

---

Réponds UNIQUEMENT avec un objet JSON valide (pas de markdown, pas de ```), avec cette structure exacte :

{{
  "api_concernee": ["nom de l'API Hub'Eau concernée parmi: {api_list}"],
  "date_source": "YYYY-MM-DD",
  "faits_techniques": [
    {{"fait": "fait technique — une particularité, limite, comportement ou erreur de l'API", "statut": "résolu|en_cours|information"}}
  ],
  "faits_metier": [
    {{"fait": "fait métier — une information sur l'hydrologie, les données, les codes, les stations", "statut": "résolu|en_cours|information"}}
  ],
  "pertinence": 3,
  "resume": "Résumé en une phrase de ce que cette issue apporte comme connaissance."
}}

Règles :
- `api_concernee` : une ou plusieurs APIs de la liste. Utilise "Général" si ça concerne toutes les APIs ou le fonctionnement global.
- `date_source` : date du dernier commentaire pertinent de l'issue, ou date de création si pas de commentaire utile. Format YYYY-MM-DD.
- `faits_techniques` : ce qu'un développeur utilisant l'API doit savoir. Chaque fait a son propre statut. Peut être vide [].
- `faits_metier` : ce qu'un hydrologue ou data scientist doit savoir sur les données. Chaque fait a son propre statut. Peut être vide [].
- `statut` par fait : "résolu" si le problème a été corrigé, "en_cours" si encore d'actualité, "information" si c'est un fait permanent.
- `pertinence` : 1=bruit/merci/ça marche, 2=info mineure, 3=utile, 4=important, 5=critique.
- Sois factuel et concis. Chaque fait doit être autonome (compréhensible sans contexte).
"""


def format_issue_for_prompt(issue: dict) -> str:
    """Format an issue dict into the extraction prompt."""
    comments_text = ""
    for c in issue.get("comments", []):
        comments_text += f"\n**{c['author']}** ({c['created_at']}):\n{c['body']}\n"

    if not comments_text:
        comments_text = "(aucun commentaire)"

    api_list = ", ".join(HUBEAU_APIS.keys())

    return EXTRACTION_PROMPT.format(
        number=issue["number"],
        title=issue["title"],
        state=issue["state"],
        labels=", ".join(issue.get("labels", [])) or "aucun",
        created_at=issue["created_at"],
        body=issue.get("body") or "(vide)",
        comments=comments_text,
        api_list=api_list,
    )


def extract_facts(client: httpx.Client, issue: dict) -> dict:
    """Send issue to Gemini and get structured facts back."""
    prompt = format_issue_for_prompt(issue)

    url = f"{GEMINI_API_BASE}/models/{GEMINI_MODEL}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2,
        },
    }

    resp = client.post(url, json=payload, params={"key": GEMINI_API_KEY})

    # Handle rate limiting
    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 10))
        print(f"  Rate limited. Waiting {retry_after}s...")
        time.sleep(retry_after)
        resp = client.post(url, json=payload, params={"key": GEMINI_API_KEY})

    resp.raise_for_status()
    result = resp.json()

    text = result["candidates"][0]["content"]["parts"][0]["text"].strip()

    # Parse JSON response
    try:
        facts = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from response if wrapped in markdown
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            facts = json.loads(match.group())
        else:
            print(f"  WARNING: Could not parse Gemini response for issue #{issue['number']}")
            facts = {
                "api_concernee": ["Général"],
                "date_source": issue.get("created_at", "")[:10],
                "faits_techniques": [],
                "faits_metier": [],
                "pertinence": 1,
                "resume": "Extraction échouée.",
                "_raw_response": text,
            }

    facts["issue_number"] = issue["number"]
    facts["issue_title"] = issue["title"]
    return facts


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract facts from fetched issues using Gemini")
    parser.add_argument("--force", action="store_true", help="Re-extract even if output exists")
    args = parser.parse_args()

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    issue_files = sorted(RAW_DATA_DIR.glob("*.json"))
    if not issue_files:
        print("No issues found in raw_data/issues/. Run fetch_issues.py first.")
        sys.exit(1)

    total = len(issue_files)
    extracted = 0
    skipped = 0

    with httpx.Client(timeout=60) as client:
        for i, filepath in enumerate(issue_files, 1):
            issue = json.loads(filepath.read_text(encoding="utf-8"))
            num = issue["number"]
            out_path = EXTRACTED_DIR / f"{num:04d}_facts.json"

            if out_path.exists() and not args.force:
                skipped += 1
                continue

            print(f"  [{i}/{total}] Extracting #{num}: {issue['title'][:60]}...")
            facts = extract_facts(client, issue)
            out_path.write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
            extracted += 1

    print(f"\nDone. Extracted: {extracted}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
