# IssueRAG Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a 3-step pipeline that fetches all GitHub issues from BRGM/hubeau, extracts structured technical and domain facts via Claude, and generates a markdown wiki organized by API.

**Architecture:** Sequential pipeline with 3 independent scripts sharing a config module. Each step reads from the previous step's output directory, making each step independently re-runnable. GitHub API for data, Claude Haiku for extraction, pure Python for wiki generation.

**Tech Stack:** Python 3.10+, httpx (HTTP client), anthropic (Claude SDK)

---

### Task 1: Project Setup

**Files:**
- Create: `requirements.txt`
- Create: `config.py`
- Create: `.gitignore`

**Step 1: Create requirements.txt**

```
httpx>=0.27
anthropic>=0.40
```

**Step 2: Create .gitignore**

```
__pycache__/
*.pyc
.env
raw_data/
extracted/
venv/
.venv/
```

**Step 3: Create config.py**

```python
"""Shared configuration for IssueRAG pipeline."""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
RAW_DATA_DIR = BASE_DIR / "raw_data" / "issues"
EXTRACTED_DIR = BASE_DIR / "extracted"
WIKI_DIR = BASE_DIR / "wiki"

# GitHub
GITHUB_REPO = "BRGM/hubeau"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_API_BASE = "https://api.github.com"

# Claude
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# Hub'Eau APIs — used for classification and wiki file mapping
HUBEAU_APIS = {
    "Hydrométrie": "hydrometrie",
    "Piézométrie": "piezometrie",
    "Qualité des cours d'eau": "qualite_cours_eau",
    "Qualité des nappes": "qualite_nappes",
    "Qualité de l'eau potable": "qualite_eau_potable",
    "Poisson": "poisson",
    "Prélèvements en eau": "prelevements",
    "Hydrobiologie": "hydrobiologie",
    "Température des cours d'eau": "temperature",
    "Écoulement des cours d'eau": "ecoulement",
    "Surveillance des eaux littorales": "eaux_littorales",
    "Indicateurs des services": "indicateurs_services",
    "Phytopharmaceutiques": "phytopharmaceutiques",
    "Général": "general",
}

# Minimum relevance score to include a fact in the wiki
MIN_RELEVANCE = 2
```

**Step 4: Create directories and install deps**

Run:
```bash
mkdir -p raw_data/issues extracted wiki
pip install -r requirements.txt
```

**Step 5: Commit**

```bash
git init
git add requirements.txt config.py .gitignore
git commit -m "chore: project setup with config, deps, and gitignore"
```

---

### Task 2: Fetch Issues Script

**Files:**
- Create: `fetch_issues.py`

**Step 1: Write fetch_issues.py**

This script fetches all issues and their comments from the GitHub API and saves them as individual JSON files.

```python
"""Fetch all issues and comments from BRGM/hubeau GitHub repo."""

import json
import sys
import time

import httpx

from config import GITHUB_API_BASE, GITHUB_REPO, GITHUB_TOKEN, RAW_DATA_DIR


def get_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def handle_rate_limit(response: httpx.Response) -> None:
    remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
    if remaining == 0:
        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset_time - int(time.time()), 1)
        print(f"  Rate limited. Waiting {wait}s...")
        time.sleep(wait)


def fetch_all_issues(client: httpx.Client) -> list[dict]:
    """Fetch all issues (open + closed), paginated."""
    all_issues = []
    page = 1
    while True:
        url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/issues"
        params = {"state": "all", "per_page": 100, "page": page}
        resp = client.get(url, params=params)
        resp.raise_for_status()
        handle_rate_limit(resp)

        issues = resp.json()
        if not issues:
            break

        # Filter out pull requests (GitHub API returns PRs as issues too)
        issues = [i for i in issues if "pull_request" not in i]
        all_issues.extend(issues)
        print(f"  Page {page}: fetched {len(issues)} issues (total: {len(all_issues)})")
        page += 1

    return all_issues


def fetch_comments(client: httpx.Client, issue_number: int) -> list[dict]:
    """Fetch all comments for a given issue."""
    comments = []
    page = 1
    while True:
        url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/issues/{issue_number}/comments"
        params = {"per_page": 100, "page": page}
        resp = client.get(url, params=params)
        resp.raise_for_status()
        handle_rate_limit(resp)

        page_comments = resp.json()
        if not page_comments:
            break

        comments.extend(page_comments)
        page += 1

    return comments


def save_issue(issue: dict, comments: list[dict]) -> None:
    """Save issue + comments as a single JSON file."""
    data = {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue.get("body", ""),
        "state": issue["state"],
        "labels": [label["name"] for label in issue.get("labels", [])],
        "author": issue["user"]["login"],
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"],
        "closed_at": issue.get("closed_at"),
        "comments_count": issue["comments"],
        "comments": [
            {
                "author": c["user"]["login"],
                "body": c["body"],
                "created_at": c["created_at"],
            }
            for c in comments
        ],
    }

    filepath = RAW_DATA_DIR / f"{issue['number']:04d}.json"
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def should_skip(issue: dict) -> bool:
    """Check if issue was already fetched and hasn't been updated."""
    filepath = RAW_DATA_DIR / f"{issue['number']:04d}.json"
    if not filepath.exists():
        return False
    existing = json.loads(filepath.read_text(encoding="utf-8"))
    return existing.get("updated_at") == issue["updated_at"]


def main() -> None:
    if not GITHUB_TOKEN:
        print("WARNING: No GITHUB_TOKEN set. Rate limit will be 60 req/h.")

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with httpx.Client(headers=get_headers(), timeout=30) as client:
        print("Fetching issues...")
        issues = fetch_all_issues(client)
        print(f"Found {len(issues)} issues total.\n")

        skipped = 0
        fetched = 0
        for i, issue in enumerate(issues, 1):
            num = issue["number"]
            if should_skip(issue):
                skipped += 1
                continue

            comments = []
            if issue["comments"] > 0:
                comments = fetch_comments(client, num)

            save_issue(issue, comments)
            fetched += 1
            print(f"  [{i}/{len(issues)}] #{num}: {issue['title'][:60]}... ({len(comments)} comments)")

        print(f"\nDone. Fetched: {fetched}, Skipped (unchanged): {skipped}")


if __name__ == "__main__":
    main()
```

**Step 2: Test the fetch script**

Run:
```bash
python fetch_issues.py
```

Expected: All issues downloaded to `raw_data/issues/`, output showing progress. Should complete in under a minute with a token.

**Step 3: Verify output**

Run:
```bash
ls raw_data/issues/ | head -5
python -c "import json; d=json.load(open('raw_data/issues/0001.json','r',encoding='utf-8')); print(d['title'], '|', len(d['comments']), 'comments')"
```

Expected: JSON files exist, content is readable with title and comments.

**Step 4: Commit**

```bash
git add fetch_issues.py
git commit -m "feat: add fetch_issues.py — downloads all GitHub issues with comments"
```

---

### Task 3: Extract Facts Script

**Files:**
- Create: `extract_facts.py`

**Step 1: Write extract_facts.py**

This script reads each raw issue JSON, sends it to Claude for structured fact extraction, and saves the result.

```python
"""Extract structured facts from issues using Claude."""

import argparse
import json
import sys

import anthropic

from config import CLAUDE_MODEL, EXTRACTED_DIR, HUBEAU_APIS, RAW_DATA_DIR

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
  "faits_techniques": [
    "fait technique 1 — une particularité, limite, comportement ou erreur de l'API à connaître",
    "fait technique 2..."
  ],
  "faits_metier": [
    "fait métier 1 — une information sur l'hydrologie, les données, les codes, les stations...",
    "fait métier 2..."
  ],
  "statut": "résolu|en_cours|information",
  "pertinence": 3,
  "resume": "Résumé en une phrase de ce que cette issue apporte comme connaissance."
}}

Règles :
- `api_concernee` : une ou plusieurs APIs de la liste. Utilise "Général" si ça concerne toutes les APIs ou le fonctionnement global.
- `faits_techniques` : ce qu'un développeur utilisant l'API doit savoir. Peut être vide [].
- `faits_metier` : ce qu'un hydrologue ou data scientist doit savoir sur les données. Peut être vide [].
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


def extract_facts(client: anthropic.Anthropic, issue: dict) -> dict:
    """Send issue to Claude and get structured facts back."""
    prompt = format_issue_for_prompt(issue)

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()

    # Parse JSON response
    try:
        facts = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from response if wrapped in markdown
        import re
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            facts = json.loads(match.group())
        else:
            print(f"  WARNING: Could not parse Claude response for issue #{issue['number']}")
            facts = {
                "api_concernee": ["Général"],
                "faits_techniques": [],
                "faits_metier": [],
                "statut": "information",
                "pertinence": 1,
                "resume": "Extraction échouée.",
                "_raw_response": text,
            }

    facts["issue_number"] = issue["number"]
    facts["issue_title"] = issue["title"]
    return facts


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract facts from fetched issues using Claude")
    parser.add_argument("--force", action="store_true", help="Re-extract even if output exists")
    args = parser.parse_args()

    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    issue_files = sorted(RAW_DATA_DIR.glob("*.json"))
    if not issue_files:
        print("No issues found in raw_data/issues/. Run fetch_issues.py first.")
        sys.exit(1)

    client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var

    total = len(issue_files)
    extracted = 0
    skipped = 0

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
```

**Step 2: Test with a single issue**

Run:
```bash
python -c "
import json, anthropic
from extract_facts import format_issue_for_prompt, extract_facts
issue = json.load(open('raw_data/issues/0001.json', 'r', encoding='utf-8'))
client = anthropic.Anthropic()
facts = extract_facts(client, issue)
print(json.dumps(facts, indent=2, ensure_ascii=False))
"
```

Expected: Valid JSON with api_concernee, faits_techniques, faits_metier, pertinence score.

**Step 3: Run full extraction**

Run:
```bash
python extract_facts.py
```

Expected: All issues processed, JSON files created in `extracted/`. Takes ~5-10 min for 276 issues with Haiku.

**Step 4: Commit**

```bash
git add extract_facts.py
git commit -m "feat: add extract_facts.py — LLM-powered fact extraction from issues"
```

---

### Task 4: Generate Wiki Script

**Files:**
- Create: `generate_wiki.py`

**Step 1: Write generate_wiki.py**

This script reads all extracted facts, groups them by API, and generates markdown files.

```python
"""Generate markdown wiki from extracted facts."""

import json
from collections import defaultdict

from config import EXTRACTED_DIR, HUBEAU_APIS, MIN_RELEVANCE, WIKI_DIR


def load_all_facts() -> list[dict]:
    """Load all extracted fact files."""
    facts = []
    for filepath in sorted(EXTRACTED_DIR.glob("*_facts.json")):
        data = json.loads(filepath.read_text(encoding="utf-8"))
        facts.append(data)
    return facts


def group_by_api(facts: list[dict]) -> dict[str, list[dict]]:
    """Group facts by API name."""
    grouped = defaultdict(list)
    for fact in facts:
        if fact.get("pertinence", 0) < MIN_RELEVANCE:
            continue
        apis = fact.get("api_concernee", ["Général"])
        if isinstance(apis, str):
            apis = [apis]
        for api in apis:
            grouped[api].append(fact)
    return dict(grouped)


def render_api_page(api_name: str, facts: list[dict]) -> str:
    """Render a single API wiki page."""
    lines = [f"# {api_name}\n"]

    # Collect all facts by category
    tech_facts = []
    metier_facts = []
    problems = []
    tips = []

    for fact in facts:
        issue_ref = f"(#{fact.get('issue_number', '?')})"

        for f in fact.get("faits_techniques", []):
            if not f:
                continue
            # Classify: if it mentions error/bug/500/erreur, it's a problem
            lower = f.lower()
            if any(w in lower for w in ["erreur", "bug", "500", "404", "problème", "échec", "fail", "broken", "cassé"]):
                problems.append(f"{f} {issue_ref}")
            elif any(w in lower for w in ["astuce", "conseil", "tip", "utiliser", "préférer", "recommand"]):
                tips.append(f"{f} {issue_ref}")
            else:
                tech_facts.append(f"{f} {issue_ref}")

        for f in fact.get("faits_metier", []):
            if f:
                metier_facts.append(f"{f} {issue_ref}")

    # Render sections
    if tech_facts:
        lines.append("## Particularités techniques\n")
        for f in tech_facts:
            lines.append(f"- {f}")
        lines.append("")

    if metier_facts:
        lines.append("## Informations métier\n")
        for f in metier_facts:
            lines.append(f"- {f}")
        lines.append("")

    if problems:
        lines.append("## Problèmes connus\n")
        for f in problems:
            lines.append(f"- {f}")
        lines.append("")

    if tips:
        lines.append("## Tips d'utilisation\n")
        for f in tips:
            lines.append(f"- {f}")
        lines.append("")

    if not any([tech_facts, metier_facts, problems, tips]):
        lines.append("*Aucun fait notable extrait pour cette API.*\n")

    # Source issues
    lines.append("---\n")
    lines.append("## Issues sources\n")
    for fact in sorted(facts, key=lambda f: f.get("issue_number", 0)):
        num = fact.get("issue_number", "?")
        title = fact.get("issue_title", "")
        resume = fact.get("resume", "")
        status = fact.get("statut", "")
        lines.append(f"- **#{num}** {title} — {resume} `[{status}]`")
    lines.append("")

    return "\n".join(lines)


def render_index(api_groups: dict[str, list[dict]]) -> str:
    """Render the wiki index page."""
    lines = [
        "# Hub'Eau — Base de connaissances\n",
        "Wiki généré automatiquement à partir des issues GitHub de [BRGM/hubeau](https://github.com/BRGM/hubeau/issues).\n",
        "## APIs\n",
    ]

    for api_name in sorted(api_groups.keys()):
        slug = HUBEAU_APIS.get(api_name, api_name.lower().replace(" ", "_").replace("'", ""))
        count = len(api_groups[api_name])
        lines.append(f"- [{api_name}]({slug}.md) ({count} issues)")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)

    facts = load_all_facts()
    if not facts:
        print("No extracted facts found. Run extract_facts.py first.")
        return

    api_groups = group_by_api(facts)

    # Generate per-API pages
    for api_name, api_facts in api_groups.items():
        slug = HUBEAU_APIS.get(api_name, api_name.lower().replace(" ", "_").replace("'", ""))
        filepath = WIKI_DIR / f"{slug}.md"
        content = render_api_page(api_name, api_facts)
        filepath.write_text(content, encoding="utf-8")
        print(f"  Generated {filepath.name} ({len(api_facts)} issues)")

    # Generate index
    index_path = WIKI_DIR / "index.md"
    index_path.write_text(render_index(api_groups), encoding="utf-8")
    print(f"  Generated index.md")

    print(f"\nDone. Wiki generated in {WIKI_DIR}/")


if __name__ == "__main__":
    main()
```

**Step 2: Run the wiki generator**

Run:
```bash
python generate_wiki.py
```

Expected: Markdown files generated in `wiki/`, one per API + index.

**Step 3: Verify output**

Run:
```bash
ls wiki/
cat wiki/index.md
cat wiki/hydrometrie.md | head -40
```

Expected: Index lists all APIs with links, API pages have 4 sections with facts and issue references.

**Step 4: Commit**

```bash
git add generate_wiki.py
git commit -m "feat: add generate_wiki.py — generates markdown wiki from extracted facts"
```

---

### Task 5: End-to-End Run and Polish

**Step 1: Full pipeline run**

Run the full pipeline end-to-end:
```bash
python fetch_issues.py
python extract_facts.py
python generate_wiki.py
```

**Step 2: Review wiki quality**

Read through the generated wiki pages and check:
- Are facts correctly categorized by API?
- Are technical facts vs. domain facts properly separated?
- Is the relevance filter working (no "merci ça marche" noise)?
- Are issue references correct?

**Step 3: Iterate on extraction prompt if needed**

If facts are miscategorized or too noisy, adjust the `EXTRACTION_PROMPT` in `extract_facts.py` and re-run with `--force`:
```bash
python extract_facts.py --force
python generate_wiki.py
```

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat: complete IssueRAG pipeline — fetch, extract, generate wiki"
```
