# Multimodal RAG learning project

This workspace starts with a matched source pair from WHO's **World Health Statistics 2024**. The report supplies prose, captions, charts and tables. Its Excel annex supplies exact country and indicator values. Both files are in [`data/raw/who_2024/`](data/raw/who_2024/). See [`data/SOURCES.md`](data/SOURCES.md) for provenance and limits.

## Learning path

1. **Inspect:** inventory PDF pages, text coverage, figures, tables and workbook sheets. Choose answerable questions before choosing models.
2. **Extract:** route native PDF text through a layout-aware parser; use OCR only for scanned regions. Preserve headings, page numbers, figure/table labels and coordinates. Read every workbook sheet with cell coordinates and data types.
3. **Normalize:** turn the varied outputs into a common `Evidence` record with `text`, `kind`, `source_file`, `page` or `sheet`/`range`, and optional `indicator`, `geography`, `year`, `unit`, `image_path` and extraction confidence. Keep the original numeric values separately.
4. **Chunk:** split prose by sections and paragraphs with small overlap. Keep each table header with its rows. Group workbook rows by a meaningful key such as indicator and geography, while retaining exact row/cell references. Never split a figure caption from its figure summary.
5. **Index:** store the text representation in a local vector store; build a keyword index over the same evidence IDs. Store numeric annex rows in SQLite or DuckDB for exact filters and calculations.
6. **Retrieve:** classify a question as narrative, lookup, aggregate, figure or mixed. Run dense and keyword searches for narrative evidence; use a structured query for exact numbers. Fuse and rerank candidates, then fetch parent context.
7. **Answer:** pass only the selected evidence to the generation model. Require citations to page or sheet/range, preserve units and data years, and say when evidence is missing. For calculations, compute in code before generation.
8. **Evaluate:** create a small question set with expected source locations. Check extraction coverage, retrieval recall, numeric equality, citation accuracy and abstention. Add handwriting cases only once a suitable source and answer key are available.

## Setup (Linux/macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-core.txt
```

`requirements-core.txt` covers the first PDF/Excel text and retrieval pass. Install `requirements-vision.txt` only when adding OCR/figure processing; it downloads large model weights on first use. No API key is required for the local embedding and Chroma options. You will still need a generation model, local or hosted, for final answers.

## Planned structure

```text
data/raw/who_2024/       original PDF and XLSX
data/processed/           extracted records, caches and figure crops
src/rag/ingestion/        PDF and spreadsheet readers
src/rag/processing/       normalization and chunking
src/rag/retrieval/        vector, keyword and structured lookup
src/rag/generation/       grounded answer construction
indexes/                  local Chroma and keyword indexes
eval/                     benchmark questions and metrics
```

`data/processed/` and `indexes/` are generated outputs and are gitignored. Raw source files are preserved with their original meaning; do not replace them with an AI-generated summary.

## Good first questions

- What does the report say about the effect of COVID-19 on life expectancy?
- What is Pakistan's 2022 age-standardized obesity prevalence in the annex? Cite the workbook row and year.
- Compare the report's discussion of air pollution with Pakistan's latest available air-pollution mortality indicator in the annex. State the annex's reference year.
- Which figure shows life expectancy by World Bank income group, and what does its caption say?

The annex is a **snapshot as of May 2024** with indicator years from 2014 to 2023. Publication year and data year must not be confused. The WHO pair does not contain a handwriting example, so a separate handwriting evaluation source is needed before claiming that capability.
