import re

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from rag.vectorstore.chroma_store import ChromaStore

def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())

class HybridRetriever:
    def __init__(self, store: ChromaStore):
        self.store = store
        self.documents = store.all_documents()

        if not self.documents:
            raise RuntimeError("Run `python -m rag.cli ingest` first.")

        tokens = [tokenize(doc.page_content) for doc in self.documents]
        self.bm25 = BM25Okapi(tokens)


    def search(self, question: str, k:int =5) -> list[Document]:
        vector_results = self.store.search(question, k=k*2)

        scores = self.bm25.get_scores(tokenize(question))
        best_rows = sorted(
            range(len(self.documents)),
            key=lambda i: scores[i],
            reverse=True,
        )[: k * 2]

        keyword_results = [
            self.documents[i]
            for i in best_rows
            if scores[i] > 0
        ]

        combined = []
        seen = set()

        for position in range(max(len(vector_results), len(keyword_results))):
            for group in (vector_results, keyword_results):
                if position < len(group):
                    doc = group[position]

                    if doc.id not in seen:
                        seen.add(doc.id)
                        combined.append(doc)

        return combined[:k]
