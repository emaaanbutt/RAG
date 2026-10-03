from langchain_core.documents import Document

from rag.config import Settings
from rag.generation.answer_generator import AnswerGenerator
from rag.ingestion.excel_loader import ExcelLoader
from rag.ingestion.pdf_loader import PdfLoader
from rag.processing.chunker import chunk_documents
from rag.retrieval.hybrid_retriever import HybridRetriever
from rag.vectorstore.chroma_store import ChromaStore


class RagPipeline:
    def __init__(self):
        self.settings = Settings()
        self.store = ChromaStore(
            self.settings.chroma_dir,
            self.settings.embedding_model,
        )
        self.retriever = None
        self.generator = None

    def ingest(self) -> int:
        documents = []

        pdf_loader = PdfLoader(self.settings.root)
        excel_loader = ExcelLoader(self.settings.root)

        for path in self.settings.raw_dir.rglob("*.pdf"):
            documents.extend(pdf_loader.load(path))

        for path in self.settings.raw_dir.rglob("*.xlsx"):
            documents.extend(excel_loader.load(path))

        if not documents:
            raise RuntimeError("No PDF or XLSX files found in data/raw.")

        chunks = chunk_documents(documents)
        self.store.rebuild(chunks)
        self.retriever = None

        return len(chunks)

    def search(self, question: str, k: int = 4) -> list[Document]:
        if not self.settings.chroma_dir.exists():
            raise RuntimeError("Build the index first with `python -m rag.cli ingest`.")
        if self.retriever is None:
            self.retriever = HybridRetriever(self.store)
        return self.retriever.search(question, k=k)

    def ask_with_sources(
        self, question: str, agentic: bool = False
    ) -> tuple[str, list[Document]]:
        if self.generator is None:
            self.generator = AnswerGenerator(
                self.settings.answer_model, self.settings.groq_api_key
            )
        search_query = self.generator.plan_search(question) if agentic else question
        documents = self.search(search_query)
        return self.generator.generate(question, documents), documents

    def ask(self, question: str, agentic: bool = False) -> str:
        answer, _ = self.ask_with_sources(question, agentic=agentic)
        return answer
