"""Utilities for managing Ollama models — load/unload for shared VRAM."""

import json
import sys

import httpx

from config import OLLAMA_HOST


def ensure_model(model: str, client: httpx.Client) -> None:
    """Pull model if not already available locally."""
    resp = client.post(f"{OLLAMA_HOST}/api/show", json={"name": model})
    if resp.status_code == 200:
        return

    print(f"  Pulling {model} (first time only)...")
    with client.stream(
        "POST", f"{OLLAMA_HOST}/api/pull", json={"name": model}
    ) as stream:
        for line in stream.iter_lines():
            data = json.loads(line)
            status = data.get("status", "")
            total = data.get("total", 0)
            completed = data.get("completed", 0)
            if total:
                pct = completed / total * 100
                print(f"\r  {status}: {pct:.0f}%", end="", flush=True)
            else:
                print(f"\r  {status}", end="", flush=True)
    print()


def unload_model(model: str, client: httpx.Client) -> None:
    """Explicitly unload model from VRAM."""
    try:
        client.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": model, "prompt": "", "keep_alive": 0},
        )
        print(f"  Unloaded {model} from VRAM")
    except httpx.HTTPError:
        pass


def chat(
    client: httpx.Client,
    model: str,
    prompt: str,
    *,
    system: str = "",
    temperature: float = 0.2,
    json_mode: bool = False,
) -> str:
    """Send a chat request to Ollama. Returns the response text.

    Uses keep_alive=0 so the model is unloaded after each response
    (shared GPU courtesy).
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload: dict = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
        "keep_alive": 0,
    }
    if json_mode:
        payload["format"] = "json"

    resp = client.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=600)
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def embed(
    client: httpx.Client,
    model: str,
    texts: list[str],
) -> list[list[float]]:
    """Get embeddings from Ollama. Returns list of vectors.

    Uses keep_alive=0 so the embedding model is unloaded after the batch.
    """
    resp = client.post(
        f"{OLLAMA_HOST}/api/embed",
        json={"model": model, "input": texts, "keep_alive": 0},
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()["embeddings"]


def check_ollama(client: httpx.Client) -> None:
    """Check that Ollama is reachable, exit if not."""
    try:
        resp = client.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        resp.raise_for_status()
    except (httpx.HTTPError, httpx.RequestError):
        print(f"ERROR: Cannot reach Ollama at {OLLAMA_HOST}")
        print("Start it with: docker compose up -d ollama")
        sys.exit(1)
