# src/tokenization.py
from __future__ import annotations
from typing import Dict, Any
import tiktoken

DEFAULT_MODEL = "gpt-3.5-turbo"

def _get_encoder(model_name: str = DEFAULT_MODEL):

    try:
        return tiktoken.encoding_for_model(model_name)
    except Exception:
        return tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str, model_name: str = DEFAULT_MODEL) -> int:

    enc = _get_encoder(model_name)
    return len(enc.encode(text or ""))

def should_chunk(num_tokens: int, context_limit: int = 4096, safety_margin: int = 512) -> bool:

    return num_tokens > (context_limit - safety_margin)

def build_article_text(item: Dict[str, Any]) -> str:

    title = (item or {}).get("title", "")
    desc = (item or {}).get("description", "")
    return f"{title}\n\n{desc}".strip()
