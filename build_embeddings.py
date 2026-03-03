"""Pre-compute embeddings for wiki content + raw facts using local Ollama.

Uses nomic-embed-text (768 dims) via Ollama.
Requires "search_document: " prefix at build time and "search_query: " prefix at query time.
"""

import json
import os
import re
import unicodedata

import httpx

import ollama_utils
from config import EXTRACTED_DIR, HUBEAU_APIS, MIN_RELEVANCE, OLLAMA_EMBED_MODEL

WIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki")
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

BATCH_SIZE = 32  # texts per Ollama call

# --- API name aliases for normalization ---
HUBEAU_API_ALIASES = {
    "qualite des nappes d'eau souterraines": "Qualité des nappes",
    "qualité des nappes d'eau souterraines": "Qualité des nappes",
    "qualite des nappes d eau souterraines": "Qualité des nappes",
    "hydro": "Hydrométrie",
    "api hydro": "Hydrométrie",
    "api hydrométrie": "Hydrométrie",
    "api hydrometrie": "Hydrométrie",
    "api piézométrie": "Piézométrie",
    "api piezometrie": "Piézométrie",
    "api qualité des cours d'eau": "Qualité des cours d'eau",
    "api qualite des cours d'eau": "Qualité des cours d'eau",
    "api poisson": "Poisson",
    "api poissons": "Poisson",
    "poissons": "Poisson",
    "api température": "Température des cours d'eau",
    "api temperature": "Température des cours d'eau",
    "température": "Température des cours d'eau",
    "temperature": "Température des cours d'eau",
    "api écoulement": "Écoulement des cours d'eau",
    "api ecoulement": "Écoulement des cours d'eau",
    "écoulement": "Écoulement des cours d'eau",
    "ecoulement": "Écoulement des cours d'eau",
    "api hydrobiologie": "Hydrobiologie",
    "api prélèvements": "Prélèvements en eau",
    "api prelevements": "Prélèvements en eau",
    "prélèvements": "Prélèvements en eau",
    "prelevements": "Prélèvements en eau",
    "eaux littorales": "Surveillance des eaux littorales",
    "api eaux littorales": "Surveillance des eaux littorales",
    "indicateurs services": "Indicateurs des services",
    "api indicateurs services": "Indicateurs des services",
    "api phytopharmaceutiques": "Phytopharmaceutiques",
    "général": "Général",
    "general": "Général",
    "api qualité de l'eau potable": "Qualité de l'eau potable",
    "api qualite de l'eau potable": "Qualité de l'eau potable",
    "eau potable": "Qualité de l'eau potable",
    "qualité eau potable": "Qualité de l'eau potable",
    "qualite eau potable": "Qualité de l'eau potable",
}


def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def normalize_api_name(name: str) -> str:
    """Normalize API name to match canonical names in HUBEAU_APIS."""
    name_lower = name.strip().lower()
    name_key = _strip_accents(name_lower)

    # Check aliases first (both with and without accents)
    if name_lower in HUBEAU_API_ALIASES:
        return HUBEAU_API_ALIASES[name_lower]
    if name_key in HUBEAU_API_ALIASES:
        return HUBEAU_API_ALIASES[name_key]

    # Check canonical names
    for canonical in HUBEAU_APIS:
        if _strip_accents(canonical.lower()) == name_key:
            return canonical

    return name


def chunk_section(text: str) -> list[str]:
    """Split a section into semantic chunks.

    - If section <= 1000 chars: return as a single chunk.
    - If section > 1000 chars: split at paragraph boundaries (double newline),
      then single newline, then sentence boundaries as fallback.
    """
    text = text.strip()
    if not text:
        return []
    if len(text) <= 1000:
        return [text]

    # Try splitting by double newline (paragraphs)
    paragraphs = re.split(r"\n\n+", text)
    if len(paragraphs) > 1:
        chunks = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(para) <= 1000:
                chunks.append(para)
            else:
                # Paragraph too large, split by sentences
                chunks.extend(_split_by_sentences(para))
        return chunks

    # Try splitting by single newline
    lines = text.split("\n")
    if len(lines) > 1:
        chunks = []
        current = []
        current_len = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if current_len + len(line) > 1000 and current:
                chunks.append("\n".join(current))
                current = []
                current_len = 0
            current.append(line)
            current_len += len(line) + 1
        if current:
            chunks.append("\n".join(current))
        return chunks

    # Fallback: split by sentences
    return _split_by_sentences(text)


def _split_by_sentences(text: str) -> list[str]:
    """Split text by sentence boundaries, grouping into chunks <= 1000 chars."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current = []
    current_len = 0
    for sent in sentences:
        if current_len + len(sent) > 1000 and current:
            chunks.append(" ".join(current))
            current = []
            current_len = 0
        current.append(sent)
        current_len += len(sent) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks


def extract_sections(filepath: str) -> list[dict]:
    """Extract sections from a wiki markdown file.

    Returns list of {text, api, section, url}.
    Now includes archive content (inside <details> blocks).
    """
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    basename = os.path.basename(filepath).replace(".md", "")
    sections = []
    current_section = ""
    current_text_lines = []
    api_name = basename

    for line in lines:
        stripped = line.strip()

        # Get API name from h1
        h1 = re.match(r"^#\s+(.+)", line)
        if h1 and not line.startswith("##"):
            api_name = h1.group(1).strip()
            continue

        # Skip details/summary HTML tags but NOT their content
        if stripped.startswith("<details") or stripped.startswith("</details>"):
            continue
        if stripped.startswith("<summary") or stripped.startswith("</summary"):
            continue

        # Detect sections
        h2 = re.match(r"^##\s+(.+)", line)
        h3 = re.match(r"^###\s+(.+)", line)

        if h2 or h3:
            # Save previous section
            if current_section and current_text_lines:
                full_text = " ".join(current_text_lines)
                if full_text.strip():
                    sections.append({
                        "text": full_text.strip(),
                        "api": api_name,
                        "section": current_section,
                        "url": basename + ".html",
                    })
            current_section = (h2 or h3).group(1).strip()
            current_text_lines = []
            continue

        # Collect text (skip metadata lines)
        if stripped and not stripped.startswith(">") and not stripped.startswith("---"):
            # Clean markdown formatting
            clean = stripped.lstrip("- ")
            clean = re.sub(r"\*\*(.+?)\*\*", r"\1", clean)
            clean = re.sub(r"~~(.+?)~~", r"\1", clean)
            clean = re.sub(r"`(.+?)`", r"\1", clean)
            clean = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", clean)
            if clean:
                current_text_lines.append(clean)

    # Don't forget last section
    if current_section and current_text_lines:
        full_text = " ".join(current_text_lines)
        if full_text.strip():
            sections.append({
                "text": full_text.strip(),
                "api": api_name,
                "section": current_section,
                "url": basename + ".html",
            })

    return sections


def load_fact_chunks() -> list[dict]:
    """Load raw facts from extracted/*_facts.json and create embeddable chunks.

    Each technical/business fact becomes an enriched chunk.
    Each issue summary also becomes a chunk.
    Only includes facts with pertinence >= MIN_RELEVANCE.
    """
    chunks = []

    for filepath in sorted(EXTRACTED_DIR.glob("*_facts.json")):
        data = json.loads(filepath.read_text(encoding="utf-8"))

        if data.get("pertinence", 0) < MIN_RELEVANCE:
            continue

        issue_num = data.get("issue_number", "?")
        issue_title = data.get("issue_title", "")
        apis = data.get("api_concernee", ["Général"])
        if isinstance(apis, str):
            apis = [apis]

        # Normalize all API names
        apis = [normalize_api_name(a) for a in apis]

        for api_name in apis:
            slug = HUBEAU_APIS.get(api_name, api_name.lower().replace(" ", "_").replace("'", ""))

            # Technical facts
            for f in data.get("faits_techniques", []):
                text, statut = _extract_fact_text(f)
                if text:
                    chunk_text = f"Issue #{issue_num}: {issue_title}. [Technique, {statut}] {text}"
                    chunks.append({
                        "text": chunk_text,
                        "api": api_name,
                        "section": f"Issue #{issue_num}",
                        "url": f"{slug}.html",
                        "source": "fact",
                    })

            # Business facts
            for f in data.get("faits_metier", []):
                text, statut = _extract_fact_text(f)
                if text:
                    chunk_text = f"Issue #{issue_num}: {issue_title}. [Métier, {statut}] {text}"
                    chunks.append({
                        "text": chunk_text,
                        "api": api_name,
                        "section": f"Issue #{issue_num}",
                        "url": f"{slug}.html",
                        "source": "fact",
                    })

            # Issue summary
            resume = data.get("resume", "")
            if resume:
                chunk_text = f"Issue #{issue_num}: {issue_title}. [Résumé] {resume}"
                chunks.append({
                    "text": chunk_text,
                    "api": api_name,
                    "section": f"Issue #{issue_num}",
                    "url": f"{slug}.html",
                    "source": "fact",
                })

    return chunks


def _extract_fact_text(f) -> tuple[str, str]:
    """Extract (text, statut) from a fact entry (dict or string)."""
    if isinstance(f, dict):
        return f.get("fait", ""), f.get("statut", "information")
    return f, "information"


def main():
    os.makedirs(SITE_DIR, exist_ok=True)

    # --- Collect wiki chunks ---
    wiki_chunks = []
    md_files = sorted(
        f for f in os.listdir(WIKI_DIR)
        if f.endswith(".md") and f != "index.md"
    )

    for filename in md_files:
        filepath = os.path.join(WIKI_DIR, filename)
        sections = extract_sections(filepath)

        for section in sections:
            text = section["text"]
            chunks = chunk_section(text)
            for chunk in chunks:
                wiki_chunks.append({
                    "text": chunk,
                    "api": section["api"],
                    "section": section["section"],
                    "url": section["url"],
                    "source": "wiki",
                })

    print(f"Extracted {len(wiki_chunks)} wiki chunks from {len(md_files)} files")

    # --- Collect fact chunks ---
    fact_chunks = load_fact_chunks()
    print(f"Extracted {len(fact_chunks)} fact chunks from extracted/")

    # --- Combine ---
    all_chunks = wiki_chunks + fact_chunks
    print(f"Total: {len(all_chunks)} chunks to embed")

    # Compute embeddings in batches via Ollama
    print(f"Computing embeddings via Ollama ({OLLAMA_EMBED_MODEL})...")
    with httpx.Client(timeout=300) as client:
        ollama_utils.check_ollama(client)
        ollama_utils.ensure_model(OLLAMA_EMBED_MODEL, client)

        for i in range(0, len(all_chunks), BATCH_SIZE):
            batch = all_chunks[i:i + BATCH_SIZE]
            texts = ["search_document: " + c["text"] for c in batch]
            embeddings = ollama_utils.embed(client, OLLAMA_EMBED_MODEL, texts)

            for j, emb in enumerate(embeddings):
                all_chunks[i + j]["embedding"] = emb

            done = min(i + BATCH_SIZE, len(all_chunks))
            print(f"  {done}/{len(all_chunks)} chunks embedded")

        ollama_utils.unload_model(OLLAMA_EMBED_MODEL, client)

    # Save
    output_path = os.path.join(SITE_DIR, "embeddings.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False)

    # Report file size
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nSaved {len(all_chunks)} embeddings to {output_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
