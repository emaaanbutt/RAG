from langchain_core.documents import Document

from rag.config import Settings
from rag.generation.answer_generator import AnswerGenerator
from rag.ingestion.excel_loader import ExcelLoader
from rag.ingestion.pdf_loader import PdfLoader
from rag.ingestion.vision_reader import VisionReader
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

    def ingest(self, use_vision: bool = False) -> int:
        documents = []

        vision = (
            VisionReader(self.settings.vision_model)
            if use_vision
            else None
        )
        pdf_loader = PdfLoader(self.settings.root, vision)
        excel_loader = ExcelLoader(self.settings.root)

        for path in self.settings.raw_dir.rglob("*.pdf"):
            documents.extend(pdf_loader.load(path))

        for path in self.settings.raw_dir.rglob("*.xlsx"):
            documents.extend(excel_loader.load(path))

        chunks = chunk_documents(documents)
        self.store.rebuild(chunks)

        return len(chunks)

    def search(self, question: str, k: int = 5) -> list[Document]:
        retriever = HybridRetriever(self.store)
        return retriever.search(question, k=k)

    def ask(self, question: str) -> str:
        documents = self.search(question)
        generator = AnswerGenerator(self.settings.answer_model)
        return generator.generate(question, documents)