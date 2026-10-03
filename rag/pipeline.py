from langchain_core.documents import Document

from rag.config import Settings
from rag.ingestion.pdf_loader import PdfLoader
from rag.ingestion.excel_loader import ExcelLoader
from rag.processing.chunker import chunk_documents
from rag.vectorstore.chroma_store import ChromaStore


class RagPipeline:
    def __init__(self):
        self.settings = Settings()
        self.store = ChromaStore(
            self.settings.chroma_dir,
            self.settings.embedding_model,
        )

    def ingest(self) -> int:
        documents = []

        pdf_loader = PdfLoader(self.settings.root)
        excel_loader = ExcelLoader(self.settings.root)

        for path in self.settings.raw_dir.rglob("*.pdf"):
            documents.extend(pdf_loader.load(path))

        for path in self.settings.raw_dir.rglob("*.xlsx"):
            documents.extend(excel_loader.load(path))

        chunks = chunk_documents(documents)
        self.store.rebuild(chunks)
        return len(chunks)

    def search(self, question: str, k: int = 5) -> list[Document]:
        return self.store.search(question, k=k)