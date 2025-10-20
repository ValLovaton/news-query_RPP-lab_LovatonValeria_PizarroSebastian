# Tarea: news-query_RPP-lab

Pipeline paso a paso:
- Paso 0: Preparación de repo (este PR)
- Paso 1: Carga de datos desde RSS de RPP (feedparser)

Requisitos:
- Python ≥ 3.10
- Instalar dependencias: `pip install -r requirements.txt`

## Paso 1: Carga de RSS (RPP)
- Dependencias: `feedparser`, `pandas`
- Notebook: `notebooks/00_load_rss.ipynb`
- Función: `src/rss_loader.py::load_rpp_rss(limit=50, export_path=None)`
- Salida (lista de dicts): `title | description | link | date_published`
- Export opcional: `data/processed/rpp_latest.json`

## Paso 2: Tokenización (tiktoken)
- Dependencias nuevas: `tiktoken`
- Módulo: `src/tokenization.py`
  - `build_article_text(item)`: une `title + description`
  - `count_tokens(text, model_name="gpt-3.5-turbo")`
  - `should_chunk(num_tokens, context_limit=4096, safety_margin=512)`
- Notebook: `notebooks/01_tokenization.ipynb`
  - Muestra tokens de una noticia y de las primeras 10
