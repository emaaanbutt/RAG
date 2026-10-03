from langchain_core.documents import Document
from openai import OpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness


class RagasEvaluator:
    def __init__(self, model_name: str, api_key: str):
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=60,
            max_retries=1,
        )
        self.metric = Faithfulness(
            llm=llm_factory(model_name, client=client, reasoning_effort="low")
        )

    def score(self, question: str, answer: str, documents: list[Document]) -> float:
        result = self.metric.score(
            user_input=question,
            response=answer,
            retrieved_contexts=[doc.page_content for doc in documents],
        )
        return float(result.value)
