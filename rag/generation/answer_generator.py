import json

from langchain_core.documents import Document
from openai import OpenAI


def source_label(doc: Document) -> str:
    metadata = doc.metadata
    label = metadata.get("source", "unknown source")
    if "page" in metadata:
        return f"{label}, PDF page {metadata['page']}"
    if "sheet" in metadata:
        return f"{label}, sheet {metadata['sheet']}, row {metadata.get('row', '?')}"
    return label


class AnswerGenerator:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=30,
            max_retries=1,
        )

    def plan_search(self, question: str) -> str:
        """Optional agent step: the Groq-hosted model chooses one search query."""
        tool = {
            "type": "function",
            "function": {
                "name": "search_documents",
                "description": "Search the indexed WHO PDF and Excel annex.",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
        }
        response = self.client.chat.completions.create(
            model=self.model_name,
            reasoning_effort="low",
            max_tokens=200,
            extra_body={"reasoning_format": "hidden"},
            messages=[
                {"role": "system", "content": "Choose a short, precise search query. Call search_documents once."},
                {"role": "user", "content": question},
            ],
            tools=[tool],
            tool_choice={"type": "function", "function": {"name": "search_documents"}},
        )
        calls = response.choices[0].message.tool_calls or []
        if not calls:
            return question
        return json.loads(calls[0].function.arguments).get("query", question)

    def generate(self, question: str, documents: list[Document]) -> str:
        if not documents:
            return "I could not find relevant evidence in the indexed documents."

        evidence = "\n\n".join(
            f"[{number}] {source_label(doc)}\n{doc.page_content}"
            for number, doc in enumerate(documents, start=1)
        )
        response = self.client.chat.completions.create(
            model=self.model_name,
            reasoning_effort="low",
            max_tokens=450,
            extra_body={"reasoning_format": "hidden"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer only from the supplied evidence. Cite factual claims with "
                        "source numbers like [1]. Preserve years, units, and age groups. "
                        "If the evidence is insufficient, say so. Do not invent numbers."
                    ),
                },
                {"role": "user", "content": f"Evidence:\n{evidence}\n\nQuestion: {question}"},
            ],
        )
        return (response.choices[0].message.content or "").strip()
