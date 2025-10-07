
# PennStateGreatValley — Unified Web Knowledge Base

![Penn State Great Valley](https://github.com/user-attachments/assets/50e5cf59-d99a-4743-b3ef-7e196322146a)

A full pipeline to **scrape, process, vectorize, and query** static & dynamic web data from the Penn State Great Valley website.  
It spans key sections — **Academics, Admissions, Professional Development, Information For** — and unifies them into a single **semantic search** experience powered by **LangChain agents** and **OpenAI**.

---

## Table of Contents
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Features](#features)
- [System Workflow](#system-workflow)
- [Repository Structure](#repository-structure)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Streamlit App](#streamlit-app)
- [Data & Metadata](#data--metadata)
- [Product Management: How We Work](#product-management-how-we-work)
- [Roadmap](#roadmap)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Quick Start

```bash
# 1) Clone
git clone https://github.com/your-username/pennstate-knowledge-base.git
cd pennstate-knowledge-base

# 2) Python environment (recommended)
python -m venv .venv && source .venv/bin/activate  # (Windows) .venv\Scripts\activate

# 3) Install
pip install -r requirements.txt

# 4) Configure API keys
cp .env.example .env   # then edit .env

# 5) Run scrapers + build vectors
python static_academic.py
python dynamic_academic.py
python create_vector_database.py
python combine_vectors.py

# 6) Launch the app
streamlit run pennstateapp.py
```

> **Tip:** If you're running locally for the first time, delete any previous vector store folders to avoid index conflicts.

---

## Architecture

```
                   ┌──────────────────────────────────────────────────┐
                   │                 Web Sources                       │
                   │  greatvalley.psu.edu/* (Academics/Admissions/…)  │
                   └───────────────┬──────────────────────────────────┘
                                   │
                       (requests/BeautifulSoup + hashing)
                                   │
                          ┌────────▼─────────┐
                          │  Raw Text Store  │  .txt/.pdf
                          └────────┬─────────┘
                                   │
                     (LangChain Text Split + Embedding)
                                   │
         ┌─────────────────────────▼─────────────────────────┐
         │                 Vector Stores                     │
         │  Chroma/FAISS per tab  → Unified Vector DB        │
         └─────────────────────────┬─────────────────────────┘
                                   │
                           (Retrieval + RAG)
                                   │
                      ┌────────────▼─────────────┐
                      │   LangChain Agent + LLM  │
                      │   (OpenAI)               │
                      └────────────┬─────────────┘
                                   │
                         ┌─────────▼──────────┐
                         │  Streamlit UI      │
                         │  (Query + Results) │
                         └────────────────────┘
```

---

## Features

### 1) Data Collection
- **Static scraping** with `requests` + **BeautifulSoup**.
- Content hashed (**SHA‑256**) to detect changes.
- Data written to simple `.txt` files for repeatable processing.

### 2) Dynamic Updates
- **Old vs New hash** comparison identifies updated pages.
- Only changed pages are re-processed to save time & cost.

### 3) Vectorization
- **RecursiveCharacterTextSplitter** chunking for context windows.
- **OpenAI embeddings** (configurable) for semantic retrieval.
- **Chroma** (default) or **FAISS** vector stores (choose per env).

### 4) Unified Knowledge Base
- Combines **Academics**, **Admissions**, **Professional Development**, **Information For** into a **single** searchable index.

### 5) Question Answering
- **LangChain Retrieval Agent** fetches relevant chunks.
- **OpenAI LLM** synthesizes grounded, cite‑able responses.

---

## System Workflow

1. **Scrape static & dynamic pages** → write `.txt` files + record **hashes**.  
2. **Detect deltas** by comparing `Hash_Code` vs `Old_Hash_Code`.  
3. **Chunk & embed** documents → write to **per‑tab** vector stores.  
4. **Combine** per‑tab stores into a **unified DB**.  
5. **Query** via Streamlit → Agent does retrieval → LLM answers.  

---

## Repository Structure

```
pennstate-knowledge-base/
├─ data/
│  ├─ raw/                      # scraped .txt/.pdf
│  ├─ vectors/                  # per-tab vector stores
│  └─ vectors_unified/          # unified vector store
├─ scripts/
│  └─ utilities/                # helpers (optional)
├─ pennstateapp.py              # Streamlit UI
├─ static_academic.py           # initial scrape
├─ dynamic_academic.py          # delta-based updates
├─ create_vector_database.py    # chunk + embed + store
├─ combine_vectors.py           # merge per-tab stores
├─ data_Updated.xlsx            # seed URLs (Sheet1..Sheet4)
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## Setup & Installation

### Prerequisites
- Python **3.8+**
- `pip`

### Install Dependencies
Your project may use either Chroma or FAISS. The example includes FAISS; you can add Chroma if desired.

```bash
pip install -r requirements.txt
# If using Chroma:
pip install chromadb
# If scraping:
pip install requests beautifulsoup4 pandas
# If you need LangChain's OpenAI package split:
pip install langchain-openai tiktoken
```

### Example `requirements.txt`
> Use this as given, or extend as needed.
```
streamlit
openai
langchain
langchain-community
faiss-cpu
python-dotenv
PyPDF2
requests
beautifulsoup4
pandas
tiktoken
```

---

## Configuration

Create a `.env` in the project root:

```
OPENAI_API_KEY=your_openai_api_key
# Optional:
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_BACKEND=chroma   # or "faiss"
```

**Seed URLs** live in `data_Updated.xlsx`:
- **Sheet1:** Academics
- **Sheet2:** Admissions
- **Sheet3:** Professional Development
- **Sheet4:** Information For

---

## Usage

### 1) Scrape & Process
```bash
python static_academic.py     # first full scrape
python dynamic_academic.py    # re-scrape only changed pages
```

### 2) Build Vector Stores
```bash
python create_vector_database.py   # per-tab stores
python combine_vectors.py          # unified store
```

### 3) Run the App
```bash
streamlit run pennstateapp.py
```

### 4) Query
Open the local URL shown in your terminal. Ask questions like:
- “List available MS programs and their admissions deadlines.”
- “Where can I contact the AI program advisor?”
- “What professional development workshops run this semester?”

---

## Streamlit App

The Streamlit UI provides:
- **Single search box** → unified retrieval
- **Top‑k results** preview
- **Answer** synthesized by LLM
- **Debug toggles** (optional): show retrieved chunks, scores, source URLs

> Consider adding session state (history), query export, and source citations for transparency.

---

## Data & Metadata

**Per page metadata**
- `Page_Name` — human‑readable label
- `Link` — source URL
- `Hash_Code` — current SHA‑256 of content
- `Old_Hash_Code` — previous SHA‑256 to detect changes

**Example**

| Page_Name | Link | Hash_Code |
|---|---|---|
| Index Page | https://greatvalley.psu.edu/ | 7021854581df7f04044cb9daad0d94eedebe4f580ec3d52feaca49e7c7 |
| Academics_Index | https://greatvalley.psu.edu/academics | 3365db13b685a64406eb3258d6d420929da05a121822d39b3d4510bd23 |
| Masters_Degree_Index | https://greatvalley.psu.edu/academics/masters-degrees | ca9542b3fb81492746b6e5184471d5747001b780d72ee736ab29fb73b7 |
| AI_Index | https://greatvalley.psu.edu/academics/masters-degrees/master-artificial-intelligence | 01fc0ae98a19b71f0471a1c817a657eb9465be46806385ea61159398a6 |
| AI_Schedule | https://greatvalley.psu.edu/academics/masters-degrees/artificial-intelligence/contact | 823732d02a9bee85ecf38a1e5c6c5f80a4a989455a8011cb24d8d47e16 |

---

## Product Management: How We Work

### Goals & Success Metrics
- **Primary Goal:** Deliver accurate, fast, and traceable answers about Penn State Great Valley.
- **KPIs:**
  - Retrieval **precision@k** and **answer groundedness** (human eval).
  - **Latency** (p95 end‑to‑end) and **cost/query**.
  - **Freshness**: % of updated pages re‑indexed within 24h.
  - **Usage**: daily active users, query completion rate.

### Users & Personas
- **Prospective Students** (discover programs, deadlines, contacts).
- **Current Students** (policies, workshops, resources).
- **Staff/Admins** (content changes, quick answers to FAQs).

### Operating Cadence
- **Weekly**: triage issues, review metrics, plan next sprint.
- **Bi‑weekly**: release cut (tag + CHANGELOG), UX check.
- **Monthly**: quality audit (sample 100 queries), roadmap review.

### Issue Labels
- `type:bug`, `type:enhancement`, `type:docs`, `type:data-source`
- `prio:P0/P1/P2`, `area:scraper/vector/app`
- `good-first-issue` for contributors

### Definition of Ready / Done
- **Ready**: user story + acceptance criteria + data impact + rollout plan.
- **Done**: tests pass, eval ≥ baseline, docs updated, feature flagged if needed.

### Release Flow
1. PR → CI checks (lint, unit, small e2e).
2. Stage with synthetic data; run eval suite.
3. Tag release, update CHANGELOG, deploy.
4. Post‑release checks and rollback plan.

### PRD Template (Short)
- **Problem:** What user outcome is missing?
- **Hypothesis:** If we do X, users will Y (metric target).
- **Scope:** In/Out, constraints.
- **Design:** UX mocks, API/DB changes.
- **Quality:** eval method, acceptance criteria.
- **Risks:** privacy, bias, drift, cost.
- **Rollout:** flag, metrics, owner, comms.

### Analytics & Evaluation
- **Query logs** (PII‑safe), **retrieval hits**, **answer length**, **model cost**.
- **Eval sets**: hand‑curated Q/A with references.
- **Canary**: small % traffic to new retriever settings.

### Privacy, Compliance, and Safety
- Respect **robots.txt** and site terms.
- Store only public content; **no PII**.
- Add **rate limits** and polite crawling (User‑Agent, backoff).
- Surface citations; enable **“view source”** links.

---

## Roadmap

- [ ] **Automated schedule** (cron/GitHub Action) for update detection.
- [ ] **Citations UI** with anchors to exact source sections.
- [ ] **Program filters** (campus, degree, delivery mode) in UI.
- [ ] **Admin dashboard**: crawl status, recency, broken links.
- [ ] **Cloud deployment** (Streamlit Cloud, Fly.io, Render, or AWS).
- [ ] **Multi‑embed support** (small vs large, cost/quality toggle).

---

## Testing

```bash
# Lint
pip install ruff pytest
ruff check .

# Unit tests (add tests/ folder)
pytest -q
```

**Manual QA**
- Run ~20 common queries and verify sources.
- Flip embedding model and re‑run small eval set.
- Modify one source page to ensure delta detection works.

---

## Troubleshooting

- **Vectors not found**: delete `data/vectors_unified/` and rebuild.
- **High cost**: reduce chunk size / top_k, or switch to `text-embedding-3-small`.
- **Scrape blocked**: add retry/backoff; honor robots and timeouts.
- **Slow answers**: enable caching; lower `k`; pre‑warm vector store.

---

## Contributing

1. Fork → feature branch.
2. Add tests/docs.
3. PR with clear description and screenshots (if UI).

---

## License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
