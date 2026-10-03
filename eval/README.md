# Evaluation

`questions.json` contains three verified questions with an expected source location and a reference answer. Run `python -m eval.run --limit 1` for a quick check or `--limit 3` for all examples.

The script reports retrieval source hit and RAGAS faithfulness. The faithfulness metric uses a Groq-hosted model as its judge and makes additional API calls. A high score means the answer is supported by the retrieved passages; it does not by itself prove that the retrieved passages are the right ones.
