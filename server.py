"""FastAPI backend for Hub'Eau RAG chatbot."""

import json
import os
import re
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
import numpy as np
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "qwen3.5:4b")
OLLAMA_EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
EMBEDDINGS_PATH = Path(os.environ.get("EMBEDDINGS_PATH", "site/embeddings.json"))

BASE_TOP_K = 5
MAX_TOP_K = 12
MIN_SCORE = 0.35
DEDUP_THRESHOLD = 0.6
MAX_HISTORY_TURNS = 4

SYSTEM_PROMPT = (
    "Tu es un assistant expert sur les APIs Hub'Eau "
    "(plateforme de donnees ouvertes sur l'eau en France, par le BRGM).\n\n"
    "Les 14 APIs Hub'Eau sont :\n"
    "- Hydrometrie (debits, hauteurs d'eau)\n"
    "- Piezometrie (niveaux des nappes)\n"
    "- Qualite des cours d'eau (analyses physico-chimiques)\n"
    "- Qualite des nappes (qualite eaux souterraines)\n"
    "- Qualite de l'eau potable\n"
    "- Poisson (donnees piscicoles)\n"
    "- Prelevements en eau\n"
    "- Hydrobiologie (IBGN, IBD, indices biologiques)\n"
    "- Temperature des cours d'eau\n"
    "- Ecoulement des cours d'eau (observations visuelles)\n"
    "- Surveillance des eaux littorales\n"
    "- Indicateurs des services (eau potable, assainissement)\n"
    "- Phytopharmaceutiques (pesticides dans l'eau)\n"
    "- General (transverse a toutes les APIs)\n\n"
    "Regles :\n"
    "- Reponds en francais, de maniere concise et structuree.\n"
    "- Base ta reponse UNIQUEMENT sur le contexte fourni et l'historique de conversation.\n"
    "- Utilise le formatage markdown : **gras** pour les points cles, `code` pour les "
    "parametres/endpoints, ### pour les sous-titres si la reponse est longue, des listes a puces.\n"
    "- Cite les numeros d'issues quand c'est pertinent, ex: (#123).\n"
    "- Structure ta reponse : d'abord une reponse directe et courte, puis les details si necessaire.\n"
    "- Si le contexte ne contient pas l'information, dis-le clairement et suggere ou chercher.\n"
    "- Si la question n'est pas liee aux APIs Hub'Eau ou a l'hydrologie, indique poliment "
    "que tu ne peux aider que sur ces sujets.\n"
    "- Pour les questions de suivi (ex: 'et pour la piezometrie ?'), utilise l'historique "
    "de conversation pour comprendre le contexte.\n"
    "- Distingue les problemes resolus (passes) des problemes encore en cours.\n"
    "- Pour les liens, utilise le format [texte](url)."
)

# Populated at startup
embed_matrix: np.ndarray | None = None  # (N, 768), L2-normalized
entries: list[dict] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    global embed_matrix, entries
    if not EMBEDDINGS_PATH.exists():
        raise RuntimeError(
            f"Embeddings file not found: {EMBEDDINGS_PATH}. "
            "Mount the site volume or run build_embeddings.py first."
        )
    raw = json.loads(EMBEDDINGS_PATH.read_text())
    vectors = []
    for item in raw:
        vectors.append(item["embedding"])
        entries.append({
            "text": item["text"],
            "api": item["api"],
            "section": item["section"],
            "url": item["url"],
            "source": item.get("source", "wiki"),
        })
    mat = np.array(vectors, dtype=np.float32)
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1e-8
    embed_matrix = mat / norms
    print(f"Loaded {len(entries)} embeddings ({embed_matrix.shape})")
    yield


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: list[dict] = Field(default=[], max_length=40)


def _get_words(text: str) -> set[str]:
    return set(
        w for w in re.sub(r"[^\w\s]", " ", text.lower()).split() if len(w) > 2
    )


def _word_overlap(words_a: set[str], words_b: set[str]) -> float:
    if not words_a:
        return 0.0
    return len(words_a & words_b) / len(words_a)


def find_similar(query_vec: np.ndarray) -> list[dict]:
    if embed_matrix is None:
        return []
    qv = query_vec / (np.linalg.norm(query_vec) + 1e-8)
    scores = embed_matrix @ qv  # (N,)

    order = np.argsort(-scores)
    selected = []
    selected_words: list[set[str]] = []

    for idx in order:
        if len(selected) >= MAX_TOP_K:
            break
        score = float(scores[idx])
        if len(selected) >= BASE_TOP_K and score < MIN_SCORE:
            break
        if score < 0.2:
            break

        entry = entries[idx]
        if entry["source"] == "fact" and selected_words:
            item_words = _get_words(entry["text"])
            if any(
                _word_overlap(item_words, sw) >= DEDUP_THRESHOLD
                for sw in selected_words
            ):
                continue

        selected.append({**entry, "score": score})
        selected_words.append(_get_words(entry["text"]))

    return selected


ALLOWED_ROLES = {"user", "assistant"}


def build_messages(
    query: str, results: list[dict], history: list[dict]
) -> list[dict]:
    context_parts = []
    for r in results:
        tag = "FAIT BRUT" if r["source"] == "fact" else r["section"]
        context_parts.append(f"[{r['api']} - {tag}] {r['text']}")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Last N turns from history — only allow user/assistant roles
    history_slice = history[-(MAX_HISTORY_TURNS * 2) :]
    for h in history_slice:
        raw_role = h.get("role", "user")
        role = "assistant" if raw_role == "bot" else raw_role
        if role not in ALLOWED_ROLES:
            continue
        content = h.get("content", "")
        if not isinstance(content, str) or not content.strip():
            continue
        messages.append({"role": role, "content": content})

    user_msg = (
        "Contexte (extraits de la base de connaissances):\n"
        + "\n\n".join(context_parts)
        + "\n\nQuestion: "
        + query
    )
    messages.append({"role": "user", "content": user_msg})
    return messages


@app.post("/api/chat")
async def chat(req: ChatRequest):
    async def generate():
        try:
            async with httpx.AsyncClient(timeout=300) as client:
                # 1. Embed query
                embed_resp = await client.post(
                    f"{OLLAMA_HOST}/api/embed",
                    json={
                        "model": OLLAMA_EMBED_MODEL,
                        "input": [f"search_query: {req.message}"],
                        "keep_alive": 0,
                    },
                )
                embed_resp.raise_for_status()
                query_vec = np.array(
                    embed_resp.json()["embeddings"][0], dtype=np.float32
                )

                # 2. RAG search
                results = find_similar(query_vec)

                # 3. Build messages
                messages = build_messages(req.message, results, req.history)

                # 4. Stream Ollama chat
                sources = [
                    {"api": r["api"], "section": r["section"], "url": r["url"]}
                    for r in results
                    if r["score"] > 0.3
                ][:3]

                async with client.stream(
                    "POST",
                    f"{OLLAMA_HOST}/api/chat",
                    json={
                        "model": OLLAMA_CHAT_MODEL,
                        "messages": messages,
                        "stream": True,
                        "think": False,
                        "options": {"temperature": 0.3, "num_predict": 2048},
                        "keep_alive": 0,
                    },
                ) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line.strip():
                            continue
                        data = json.loads(line)
                        token = data.get("message", {}).get("content", "")
                        if token:
                            yield json.dumps({"token": token}) + "\n"

                yield json.dumps({"done": True, "sources": sources}) + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "embeddings_loaded": embed_matrix is not None,
        "num_entries": len(entries),
    }
