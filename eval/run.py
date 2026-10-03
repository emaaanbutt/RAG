import argparse
import json
from pathlib import Path

from eval.evaluator import RagasEvaluator
from rag.config import Settings
from rag.pipeline import RagPipeline


def source_hit(documents, case: dict) -> bool:
    for doc in documents:
        metadata = doc.metadata
        if not metadata.get("source", "").endswith(case["source"]):
            continue
        if all(metadata.get(key) == case[key] for key in ("page", "sheet", "row") if key in case):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Small RAGAS evaluation set")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    cases = json.loads((Path(__file__).parent / "questions.json").read_text())[: args.limit]
    settings = Settings()
    rag = RagPipeline()
    evaluator = RagasEvaluator(settings.answer_model, settings.groq_api_key)

    for case in cases:
        answer, documents = rag.ask_with_sources(case["question"])
        hit = source_hit(documents, case)
        faithfulness = evaluator.score(case["question"], answer, documents)
        print(f"\nQuestion: {case['question']}")
        print(f"Answer: {answer}")
        print(f"Expected: {case['reference']}")
        print(f"Expected source in top results: {hit}")
        print(f"RAGAS faithfulness: {faithfulness:.2f}")


if __name__ == "__main__":
    main()
