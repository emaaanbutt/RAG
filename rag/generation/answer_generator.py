from langchain_core.documents import Document


class AnswerGenerator:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate(self, question: str, documents: list[Document]) -> str:
        if not documents:
            return "I did not find the answer to this question.."

        evidence = []
        source_key = []

        for number, doc in enumerate(documents, start=1):
            metadata = doc.metadata
            location = metadata.get("source", "unknown source")

            if "page" in metadata:
                location += f", PDF page {metadata['page']}"
            elif "sheet" in metadata:
                location += (
                    f", sheet {metadata['sheet']}, "
                    f"row {metadata.get('row', '?')}"
                )

            evidence.append(
                f"[{number}] {location}\n{doc.page_content}"
            )
            source_key.append(f"[{number}] {location}")

        context = "\n\n".join(evidence)

        messages = [
            {
                "role": "system",
                "content": (
                    "Answer using only the supplied evidence. "
                    "Cite evidence numbers such as [1]. "
                    "If the evidence does not contain the answer, say so. "
                    "Never invent numbers."
                ),
            },
            {
                "role": "user",
                "content": f"Evidence:\n{context}\n\nQuestion: {question}",
            },
        ]

        from transformers import pipeline

        model = pipeline("text-generation", model=self.model_name)
        result = model(messages, max_new_tokens=250, do_sample=False)
        answer = result[0]["generated_text"][-1]["content"].strip()

        return answer + "\n\nSource key:\n" + "\n".join(source_key)