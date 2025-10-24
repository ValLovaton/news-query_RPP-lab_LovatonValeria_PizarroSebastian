# News Retrieval & Embedding System — RPP Perú

## Objetivo General
Desarrollar un sistema modular que recupere y procese automáticamente las noticias más recientes de RPP Perú ([https://rpp.pe/rss](https://rpp.pe/rss)), las vectorice con modelos de *sentence embeddings* y permita realizar búsquedas semánticas mediante langChain* y ChromaDB.

Este repositorio corresponde al Task 1 — News Retrieval and Embedding System del laboratorio.

##  Requisitos técnicos
* Python ≥ 3.10
* Ejecución recomendada: Google Colab o Jupyter Notebook
* Instalar dependencias:
  ```
  pip install -r requirements.txt
  ```
---
## Estructura del repositorio

```
news-query_RPP-lab/
│
├─ data/
│   └─ processed/
│       └─ rpp_latest.json             # Últimas 50 noticias exportadas
│
├─ notebooks/
│   ├─ 00_load_rss.ipynb               # Descarga del RSS con feedparser
│   ├─ 01_tokenization.ipynb           # Tokenización y conteo de tokens
│   ├─ 02_embeddings_retrieval.ipynb   # Embeddings + almacenamiento Chroma
│   └─ 03_pipeline_langchain.ipynb     
│
├─ src/
│   ├─ rss_loader.py                   # Carga y exportación RSS
│   ├─ tokenization.py                 # Funciones de conteo y chunking
│   ├─ embeddings_store.py             # Embeddings y Chroma upsert
│   └─ langchain_pipeline.py           # Orquestación con LangChain
│
├─ outputs/
│   └─ sample_query.csv                # Ejemplo de consulta “economía”
│
├─ .gitignore
├─ requirements.txt
└─ README.md
```

## Pipeline paso a paso

### Preparación: Clonar y ejecutar en Colab:

```
!git clone https://github.com/ValLovaton/news-query_RPP-lab_LovatonValeria_PizarroSebastian.git
%cd news-query_RPP-lab_LovatonValeria_PizarroSebastian
!pip install -r requirements.txt
```

---

### Carga de datos (feedparser)

**Notebook:** 00_load_rss.ipynb
**Script:** src/rss_loader.py::load_rpp_rss(limit=50, export_path)

* Se extrajeron 50 noticias del feed de RPP.
* Campos: title, description, link, date_published.
* Archivo exportado: data/processed/rpp_latest.json.

Ejemplo de salida:

| title                                               | description                                                         | link                                                                            | date_published                 |
| --------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------ |
| Latin Billboard 2025: Bad Bunny consigue su pr…     | ¡Arriba Puerto Rico! Bad Bunny se consagró en…                      | [https://rpp.pe/musica/internacional/](https://rpp.pe/musica/internacional/)... | Thu 23 Oct 2025 20:32:56 −0500 |
| Premier descartó reapertura del penal de El Frontón | El premier Ernesto Álvarez afirmó que es una decisión del gobierno… | [https://rpp.pe/politica/gobierno/](https://rpp.pe/politica/gobierno/)...       | Thu 23 Oct 2025 19:52:50 −0500 |

### Tokenización (tiktoken)

**Notebook:** 01_tokenization.ipynb
**Script:** src/tokenization.py

* Modelo de referencia: gpt-3.5-turbo (encodificación cl100k_base).
* Conteo promedio: **70 – 90 tokens** por noticia.
* Ningún texto excede el límite de 4096 tokens → need_chunk = False.

Ejemplo de resultado:
```
{'tokens': 93, 'need_chunk': False}
```

### Embeddings y almacenamiento en ChromaDB

**Notebook:** 02_embeddings_retrieval.ipynb
**Script:** src/embeddings_store.py

* Modelo: sentence-transformers/all-MiniLM-L6-v2
* Dimensión del embedding: 384
* Embeddings normalizados (cosine similarity).
* Base vectorial creada con persistencia local `.chroma/`.

**Configuración usada:**
collection_name = "rpp_news"
persist_directory = ".chroma/"

---

### Recuperación semántica (LangChain Retriever)

**Notebook:** 03_pipeline_langchain.ipynb
**Script:** src/langchain_pipeline.py

* Pipeline modular: Load → Tokenize → Embed → Store → Retrieve
* Función principal:
  ```
  run_pipeline(query="Últimas noticias de economía", limit=50)
  ```
* Resultado: tabla con las noticias más relevantes según similitud semántica.

Ejemplo de salida (query="Últimas noticias de economía"):

| title                                            | description                                  | link                                                    | date_published                 |
| ------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------- | ------------------------------ |
| BCR eleva proyección de crecimiento para 2025    | El presidente del Banco Central indicó que … | [https://rpp.pe/economia/](https://rpp.pe/economia/)... | Thu 23 Oct 2025 12:40:00 −0500 |
| Dólar retrocede por mayor flujo de exportaciones | Cotización interbancaria cerró a S/ 3.65 …   | [https://rpp.pe/economia/](https://rpp.pe/economia/)... | Thu 23 Oct 2025 09:15:00 −0500 |

---

## Resultados globales

| Etapa                       | Resultado                                                |
| --------------------------- | -------------------------------------------------------- |
| Noticias descargadas        | 50                                                       |
| Tokens promedio por noticia | ≈ 80                                                     |
| Necesidad de chunking       | No                                                       |
| Modelo de embeddings        | all-MiniLM-L6-v2                                         |
| Vector store                | Chroma (persistente)                                     |
| Consulta de ejemplo         | “Últimas noticias de economía”                           |
| Salida                      | DataFrame (4 columnas) + CSV en outputs/sample_query.csv |


