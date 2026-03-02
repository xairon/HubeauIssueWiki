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
