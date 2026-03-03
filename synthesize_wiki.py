"""Generate synthesized wiki with Guide + Archive from extracted facts."""

import json
import re
import sys
from collections import defaultdict

import httpx
import unicodedata

import ollama_utils
from config import (
    EXTRACTED_DIR,
    HUBEAU_APIS,
    HUBEAU_API_ALIASES,
    MIN_RELEVANCE,
    OLLAMA_BIG_MODEL,
    WIKI_DIR,
)

SYNTHESIS_PROMPT = """\
Tu es un expert en hydrologie et en APIs de données environnementales. Tu rédiges un guide pratique pour les développeurs et data scientists qui utilisent l'API Hub'Eau "{api_name}".

Voici {count} faits extraits de {issue_count} issues GitHub. Chaque fait a un statut (résolu/en_cours/information), une date source et un score de pertinence (1-5).

## Faits bruts

{facts_text}

---

À partir de ces faits, rédige un guide structuré en prose concise. **Distingue clairement** ce qui est encore vrai aujourd'hui de ce qui a été corrigé/résolu dans le passé.

Réponds UNIQUEMENT avec du markdown valide (PAS de JSON), structuré exactement comme suit :

### Comportement actuel

Décris le fonctionnement actuel de l'API : endpoints principaux, format des données, pagination, paramètres importants. Ne mentionne que ce qui est **encore vrai**. Fusionne les faits redondants. Écris au présent.

### Pièges à éviter

Liste les limitations, comportements surprenants et erreurs fréquentes qui sont **encore d'actualité**. Pour chaque piège, explique brièvement pourquoi c'est un problème et comment le contourner.

### Bonnes pratiques

Donne des conseils concrets et actionnables pour bien utiliser l'API. Basé sur les retours d'expérience des utilisateurs.

### Contexte métier

Explique les concepts hydrologiques ou de données nécessaires pour comprendre et utiliser correctement cette API (codes BSS, SANDRE, types de stations, sources de données, etc.). Ce qui est utile pour un non-spécialiste.

### Évolutions récentes

Changements notables récents concernant cette API, classés par date (du plus récent au plus ancien). Inclus les corrections de bugs, nouvelles fonctionnalités, changements de comportement. Utilise les dates sources des faits pour le classement.

### Historique notable

Problèmes importants qui ont été résolus dans le passé et qu'il est utile de connaître (pour ne pas perdre de temps à les re-diagnostiquer, ou pour comprendre l'évolution de l'API). Mentionne la date de résolution si disponible.

Règles :
- Écris en français, en prose (pas juste des listes à puces)
- Sois concis : chaque section fait 3-10 lignes max
- Ne répète pas les mêmes infos entre sections
- Les faits marqués "résolu" vont dans "Historique notable" s'ils sont importants, sinon ils sont ignorés
- Les faits marqués "en_cours" ou "information" vont dans les sections appropriées (Comportement actuel, Pièges, Bonnes pratiques, Contexte métier)
- Cite les numéros d'issues entre parenthèses quand c'est pertinent, ex: (#123)
- Si une section serait vide, écris juste "*Rien de notable.*"
"""


def normalize_api_name(name: str) -> str:
    """Normalize API name to match canonical names in HUBEAU_APIS.

    Checks aliases first, then canonical names.
    Both checks are accent-insensitive and case-insensitive.
    """
    def strip_accents(s: str) -> str:
        return "".join(
            c for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        )

    name_stripped = name.strip()
    name_lower = name_stripped.lower()
    name_key = strip_accents(name_lower)

    # Check aliases (case-insensitive + accent-insensitive)
    for alias, canonical in HUBEAU_API_ALIASES.items():
        if name_lower == alias.lower() or name_key == strip_accents(alias.lower()):
            return canonical

    # Check canonical names
    for canonical in HUBEAU_APIS:
        if strip_accents(canonical.lower()) == name_key:
            return canonical

    return name_stripped


def load_all_facts() -> list[dict]:
    """Load all extracted fact files."""
    facts = []
    for filepath in sorted(EXTRACTED_DIR.glob("*_facts.json")):
        data = json.loads(filepath.read_text(encoding="utf-8"))
        facts.append(data)
    return facts


def group_by_api(facts: list[dict]) -> dict[str, list[dict]]:
    """Group facts by API name, filtering by relevance."""
    grouped = defaultdict(list)
    for fact in facts:
        if fact.get("pertinence", 0) < MIN_RELEVANCE:
            continue
        apis = fact.get("api_concernee", ["Général"])
        if isinstance(apis, str):
            apis = [apis]
        for api in apis:
            api = normalize_api_name(api)
            grouped[api].append(fact)
    return dict(grouped)


def _extract_fact_text(f) -> tuple[str, str]:
    """Extract (text, statut) from a fact entry (dict or string)."""
    if isinstance(f, dict):
        return f.get("fait", ""), f.get("statut", "information")
    return f, "information"


def format_facts_for_synthesis(facts: list[dict]) -> str:
    """Format all facts of an API into text for the synthesis prompt."""
    lines = []
    for fact in sorted(facts, key=lambda f: f.get("issue_number", 0)):
        num = fact.get("issue_number", "?")
        title = fact.get("issue_title", "")
        date_source = fact.get("date_source", "")
        pertinence = fact.get("pertinence", 3)

        header = f"### Issue #{num}: {title} [date: {date_source}, pertinence: {pertinence}/5]"
        lines.append(header)

        for f in fact.get("faits_techniques", []):
            text, statut = _extract_fact_text(f)
            if text:
                lines.append(f"- [TECHNIQUE | {statut}] {text}")
        for f in fact.get("faits_metier", []):
            text, statut = _extract_fact_text(f)
            if text:
                lines.append(f"- [MÉTIER | {statut}] {text}")

        resume = fact.get("resume", "")
        if resume:
            lines.append(f"- [RÉSUMÉ] {resume}")
        lines.append("")

    return "\n".join(lines)


def synthesize_guide(client: httpx.Client, api_name: str, facts: list[dict]) -> str:
    """Call Ollama to synthesize a guide from all facts of an API."""
    facts_text = format_facts_for_synthesis(facts)
    total_facts = sum(
        len(f.get("faits_techniques", [])) + len(f.get("faits_metier", []))
        for f in facts
    )

    prompt = SYNTHESIS_PROMPT.format(
        api_name=api_name,
        count=total_facts,
        issue_count=len(facts),
        facts_text=facts_text,
    )

    return ollama_utils.chat(client, OLLAMA_BIG_MODEL, prompt, temperature=0.3)


def render_archive(facts: list[dict]) -> str:
    """Render the archive section with raw facts."""
    lines = []

    # Split into current vs resolved
    current_facts = []
    resolved_facts = []

    for fact in facts:
        issue_ref = f"(#{fact.get('issue_number', '?')})"

        for f in fact.get("faits_techniques", []):
            text, statut = _extract_fact_text(f)
            if text:
                entry = f"{text} {issue_ref}"
                if statut == "résolu":
                    resolved_facts.append(entry)
                else:
                    current_facts.append(entry)

        for f in fact.get("faits_metier", []):
            text, statut = _extract_fact_text(f)
            if text:
                entry = f"{text} {issue_ref}"
                if statut == "résolu":
                    resolved_facts.append(entry)
                else:
                    current_facts.append(entry)

    if current_facts:
        lines.append("### Faits actuels\n")
        for f in current_facts:
            lines.append(f"- {f}")
        lines.append("")

    if resolved_facts:
        lines.append("### Historique des problèmes résolus\n")
        for f in resolved_facts:
            lines.append(f"- ~~{f}~~")
        lines.append("")

    # Issue sources
    lines.append("### Issues sources\n")
    for fact in sorted(facts, key=lambda f: f.get("issue_number", 0)):
        num = fact.get("issue_number", "?")
        title = fact.get("issue_title", "")
        resume = fact.get("resume", "")
        date_source = fact.get("date_source", "")
        date_label = f" ({date_source})" if date_source else ""
        lines.append(f"- **#{num}** {title}{date_label} — {resume}")
    lines.append("")

    return "\n".join(lines)


def render_api_page(api_name: str, guide_text: str, facts: list[dict]) -> str:
    """Render a full API page with Guide + Archive."""
    lines = [
        f"# {api_name}\n",
        f"> {len(facts)} issues analysées\n",
        "## Guide\n",
        guide_text,
        "",
        "---\n",
        "<details>",
        "<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>\n",
        render_archive(facts),
        "</details>",
        "",
    ]
    return "\n".join(lines)


def render_index(api_groups: dict[str, list[dict]]) -> str:
    """Render the wiki index page. Sorts APIs alphabetically with Général last."""
    lines = [
        "# Hub'Eau — Base de connaissances\n",
        "Guide pratique et archive des connaissances extraites des issues GitHub de [BRGM/hubeau](https://github.com/BRGM/hubeau/issues).\n",
        "Chaque page contient un **guide synthétique** (ce qui est encore vrai et actionnable) et une **archive détaillée** (tous les faits bruts avec références).\n",
        "## APIs\n",
    ]

    # Sort with "Général" last
    api_names = sorted(api_groups.keys(), key=lambda n: (n == "Général", n))

    for api_name in api_names:
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
        sys.exit(1)

    api_groups = group_by_api(facts)
    print(f"Found {len(api_groups)} APIs to synthesize.\n")

    with httpx.Client(timeout=600) as client:
        ollama_utils.check_ollama(client)
        ollama_utils.ensure_model(OLLAMA_BIG_MODEL, client)

        for api_name, api_facts in api_groups.items():
            slug = HUBEAU_APIS.get(api_name, api_name.lower().replace(" ", "_").replace("'", ""))
            filepath = WIKI_DIR / f"{slug}.md"

            print(f"  Synthesizing {api_name} ({len(api_facts)} issues)...")
            guide_text = synthesize_guide(client, api_name, api_facts)

            content = render_api_page(api_name, guide_text, api_facts)
            filepath.write_text(content, encoding="utf-8")
            print(f"    -> {filepath.name}")

        ollama_utils.unload_model(OLLAMA_BIG_MODEL, client)

    # Generate index
    index_path = WIKI_DIR / "index.md"
    index_path.write_text(render_index(api_groups), encoding="utf-8")
    print(f"  Generated index.md")

    # Clean up orphan .md files that don't correspond to any canonical API
    canonical_slugs = set(HUBEAU_APIS.values())
    canonical_slugs.add("index")
    for md_file in WIKI_DIR.glob("*.md"):
        slug = md_file.stem
        if slug not in canonical_slugs:
            md_file.unlink()
            print(f"  Removed orphan: {md_file.name}")

    print(f"\nDone. Wiki v2 generated in {WIKI_DIR}/")


if __name__ == "__main__":
    main()
