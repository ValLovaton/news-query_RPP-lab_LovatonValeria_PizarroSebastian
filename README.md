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
