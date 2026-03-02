"""Pre-compute embeddings for wiki content using HuggingFace Inference API.

Uses BAAI/bge-small-en-v1.5 (384 dims) — available as Xenova/bge-small-en-v1.5
in Transformers.js, ensuring vector space compatibility between build-time and browser.
"""

import json
import os
import re
import time

import httpx

WIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki")
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_MODEL = "BAAI/bge-small-en-v1.5"
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"
CHUNK_SIZE = 500  # characters per chunk
CHUNK_OVERLAP = 50
BATCH_SIZE = 32  # texts per API call


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks


def extract_sections(filepath: str) -> list[dict]:
    """Extract sections from a wiki markdown file.

    Returns list of {text, api, section, url}.
    """
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    basename = os.path.basename(filepath).replace(".md", "")
    sections = []
    current_section = ""
    current_text_lines = []
    api_name = basename
    in_details = False

    for line in lines:
        stripped = line.strip()

        # Get API name from h1
        h1 = re.match(r"^#\s+(.+)", line)
        if h1 and not line.startswith("##"):
            api_name = h1.group(1).strip()
            continue

        # Track details block
        if stripped.startswith("<details"):
            in_details = True
            continue
        if stripped.startswith("</details>"):
            in_details = False
            continue
        if stripped.startswith("<summary") or stripped.startswith("</summary"):
            continue

        # Skip archive section (inside details) for embeddings
        if in_details:
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


def get_embeddings_batch(texts: list[str], client: httpx.Client) -> list[list[float]]:
    """Get embeddings for a batch of texts via HuggingFace Inference API."""
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
    }

    for attempt in range(3):
        resp = client.post(HF_API_URL, json={"inputs": texts}, headers=headers)

        if resp.status_code == 503:
            data = resp.json()
            wait = data.get("estimated_time", 20)
            print(f"    Model loading, waiting {wait:.0f}s...")
            time.sleep(wait)
            continue

        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 10))
            print(f"    Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue

        resp.raise_for_status()
        result = resp.json()

        # API returns [[float]] for each text — may need mean pooling
        embeddings = []
        for item in result:
            if isinstance(item[0], list):
                # Token-level embeddings, need mean pooling
                n_tokens = len(item)
                dim = len(item[0])
                pooled = [0.0] * dim
                for token_emb in item:
                    for j in range(dim):
                        pooled[j] += token_emb[j]
                pooled = [v / n_tokens for v in pooled]
                # Normalize
                norm = sum(v * v for v in pooled) ** 0.5
                if norm > 0:
                    pooled = [v / norm for v in pooled]
                embeddings.append(pooled)
            else:
                # Already pooled
                embeddings.append(item)
        return embeddings

    raise RuntimeError("Failed to get embeddings after 3 attempts")


def main():
    if not HF_TOKEN:
        print("ERROR: HF_TOKEN environment variable not set.")
        return

    os.makedirs(SITE_DIR, exist_ok=True)

    # Collect all chunks from wiki files
    all_chunks = []
    md_files = sorted(
        f for f in os.listdir(WIKI_DIR)
        if f.endswith(".md") and f != "index.md"
    )

    for filename in md_files:
        filepath = os.path.join(WIKI_DIR, filename)
        sections = extract_sections(filepath)

        for section in sections:
            text = section["text"]
            chunks = chunk_text(text)
            for chunk in chunks:
                all_chunks.append({
                    "text": chunk,
                    "api": section["api"],
                    "section": section["section"],
                    "url": section["url"],
                })

    print(f"Extracted {len(all_chunks)} chunks from {len(md_files)} files")

    # Compute embeddings in batches
    print("Computing embeddings via HuggingFace API...")
    with httpx.Client(timeout=120) as client:
        for i in range(0, len(all_chunks), BATCH_SIZE):
            batch = all_chunks[i:i + BATCH_SIZE]
            texts = [c["text"] for c in batch]
            embeddings = get_embeddings_batch(texts, client)

            for j, emb in enumerate(embeddings):
                all_chunks[i + j]["embedding"] = emb

            done = min(i + BATCH_SIZE, len(all_chunks))
            print(f"  {done}/{len(all_chunks)} chunks embedded")

    # Save
    output_path = os.path.join(SITE_DIR, "embeddings.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False)

    # Report file size
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nSaved {len(all_chunks)} embeddings to {output_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
