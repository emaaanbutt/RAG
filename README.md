# RAG Bot

This learning project answers questions from the WHO *World Health Statistics 2024* PDF and its Excel annex in `data/raw/who_2024/`.

## How it works

1. `rag/ingestion/` reads selectable PDF text, PDF tables, and Excel rows.
2. `rag/processing/chunker.py` splits long documents while preserving source metadata.
3. `rag/vectorstore/chroma_store.py` saves embeddings and text in local Chroma.
4. `rag/retrieval/hybrid_retriever.py` combines vector and BM25 keyword results.
5. `rag/generation/answer_generator.py` asks a Groq-hosted model to answer from the retrieved text, with citations.

The optional **Agentic search** switch asks the model to choose a search query before retrieval. It makes one extra API call. Normal mode is faster and uses one Groq call per answer. OCR is outside this version's scope.

## Setup

A `.venv` already exists in this workspace. For a new checkout, create one:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Edit the project `.env` file and paste your Groq API key after `GROQ_API_KEY=`. `.env` is ignored by Git. `GROQ_MODEL` defaults to `openai/gpt-oss-20b`, hosted by Groq. The Python `openai` package is used only as an OpenAI-compatible client; requests go to `api.groq.com`.

```text
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Build the local index once. The first run downloads the embedding model, so it takes longer than asking questions. The existing index can be reused across app restarts.

```bash
python -m rag.cli ingest
python -m rag.cli search "What does Figure 1.3 compare?"
python -m rag.cli ask "What does Figure 1.3 compare?"
python -m rag.cli ask --agentic "What does Figure 1.3 compare?"
streamlit run app.py
```

If the Hugging Face model is already cached and network checks are slow, run commands with `HF_HUB_OFFLINE=1`.

## Evaluation

The app's **Evaluate last answer with RAGAS** button and `eval/run.py` report *faithfulness*: whether the answer is supported by retrieved text. The batch script also checks whether the expected PDF page or workbook row appeared in retrieval. Evaluation makes extra Groq API calls.

```bash
python -m eval.run --limit 1
python -m eval.run --limit 3
```

The sample questions and reference answers are in `eval/questions.json`. RAGAS scores are useful diagnostics, not proof that every answer is correct. Check the cited PDF page or workbook row for important answers.

## Limits

- The PDF reader works with selectable text and table extraction. It does not perform OCR on scanned or handwritten pages.
- For exact Excel totals or averages, calculate from workbook cells in Python; the answer model should not invent arithmetic.
- The first query in a new process loads the local embedding model. Streamlit caches the pipeline so later questions avoid that startup cost.
