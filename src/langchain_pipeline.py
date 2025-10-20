# src/langchain_pipeline.py
from __future__ import annotations
from typing import List, Dict, Any
import pandas as pd

# Reuso de módulos previos
from src.rss_loader import load_rpp_rss
from src.tokenization import build_article_text, count_tokens, should_chunk
from src.embeddings_store import to_documents, upsert_chroma, build_retriever, query_retriever, results_to_df

# --- Orquestación "tipo cadena" (simple y explícita) ---

def run_ingest(limit: int = 50) -> List[Dict[str, Any]]:
    """Carga items desde el RSS de RPP."""
    return load_rpp_rss(limit=limit)

def run_tokenize_preview(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Toma el primer item, arma el texto y calcula tokens + flag de chunking."""
    if not items:
        return {"tokens": 0, "need_chunk": False, "preview": ""}
    text = build_article_text(items[0])
    tokens = count_tokens(text, model_name="gpt-3.5-turbo")
    return {"tokens": tokens, "need_chunk": should_chunk(tokens), "preview": text[:300]}

def run_embed_store(items: List[Dict[str, Any]], persist_dir: str = ".chroma", collection_name: str = "rpp_news") -> Any:
    """Convierte items a Document, genera embeddings y persiste en Chroma."""
    docs = to_documents(items)
    vs = upsert_chroma(docs, persist_dir=persist_dir, collection_name=collection_name)
    return vs

def run_retrieve(vs, query: str, k: int = 8) -> pd.DataFrame:
    """Construye retriever, ejecuta la consulta y devuelve DataFrame con columnas pedidas."""
    retriever = build_retriever(vs, k=k)
    docs = query_retriever(retriever, query)
    return results_to_df(docs)

def run_pipeline(query: str = "Últimas noticias de economía", limit: int = 50,
                 persist_dir: str = ".chroma", collection_name: str = "rpp_news") -> Dict[str, Any]:
    """Pipeline end-to-end: load → tokenize (preview) → embed/store → retrieve → DataFrame."""
    items = run_ingest(limit=limit)
    tok = run_tokenize_preview(items)
    vs = run_embed_store(items, persist_dir=persist_dir, collection_name=collection_name)
    df = run_retrieve(vs, query=query, k=8)
    return {"tokenization": tok, "results": df}