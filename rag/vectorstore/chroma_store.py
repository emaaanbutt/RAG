import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from rag.embeddings.embedder import Embedder

class ChromaStore:
    def __init__(self, directory: Path, embedding_model: str):
        self.directory = directory
        self.embedder = Embedder(embedding_model)
        self.db = None

    def _open(self) -> Chroma:
        if self.db is None:
            self.db = Chroma(
                collection_name = "rag_evidence",
                embedding_function = self.embedder.create(),
                persist_directory=str(self.directory)
            )

        return self.db


    def rebuild(self, documents: list[Document], batch_size: int = 128) -> None:
        if self.directory.exists():
            shutil.rmtree(self.directory)

        self.db = None
        db = self._open()

        for start in range(0, len(documents), batch_size):
            batch = documents[start:start + batch_size]
            db.add_documents(batch)

    def search(
        self,
        question: str,
        k: int = 25,
    ) -> list[Document]:
        return self._open().similarity_search(
            question,
            k=k,
        )

    
