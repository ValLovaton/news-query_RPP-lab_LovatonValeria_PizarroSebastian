# src/embeddings_store.py
from __future__ import annotations
from typing import List, Dict, Any
import pandas as pd

# LangChain & Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def to_documents(items: List[Dict[str, Any]]) -> List[Document]:
    """Convierte items RSS en Documentos de LangChain (contenido = title + description)."""
    docs: List[Document] = []
    for r in items:
        page_content = f"{r.get('title','')}\n\n{r.get('description','')}"
        metadata = {
            "title": r.get("title", ""),
            "description": r.get("description", ""),
            "link": r.get("link", ""),
            "date_published": r.get("date_published", ""),
            "source": "RPP RSS",
        }
        docs.append(Document(page_content=page_content, metadata=metadata))
    return docs

def get_embeddings():
    """Embeddings HF (all-MiniLM-L6-v2)."""
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def upsert_chroma(docs: List[Document], persist_dir: str = ".chroma", collection_name: str = "rpp_news") -> Chroma:
    """Crea o actualiza una colección Chroma con los documentos."""
    embeddings = get_embeddings()
    vs = Chroma(collection_name=collection_name, embedding_function=embeddings, persist_directory=persist_dir)
    # Upsert mediante add_documents (idempotencia básica si re-corre no es crítica en el lab)
    if docs:
        vs.add_documents(docs)
        vs.persist()
    return vs

def build_retriever(vs: Chroma, k: int = 8):
    """Devuelve un retriever de similitud con top-k."""
    return vs.as_retriever(search_kwargs={"k": k})

def query_retriever(retriever, query: str):
    """Ejecuta búsqueda en lenguaje natural y devuelve Document[]."""
    return retriever.get_relevant_documents(query)

def results_to_df(docs: List[Document]) -> pd.DataFrame:
    """Convierte la lista de Document en un DataFrame con columnas pedidas."""
    rows = []
    for d in docs:
        m = d.metadata or {}
        rows.append({
            "title": m.get("title", ""),
            "description": m.get("description", ""),
            "link": m.get("link", ""),
            "date_published": m.get("date_published", ""),
        })
    return pd.DataFrame(rows)
