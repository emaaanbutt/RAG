from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

@dataclass(frozen=True)
class Settings:
    root: Path = ROOT

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    answer_model: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    chunk_size: int = 700
    chunk_overlap: int = 100

    @property
    def raw_dir(self) -> Path:
        return self.root / "data" / "raw"

    @property
    def index_dir(self) -> Path:
        return self.root / "indexes"

    @property
    def chroma_dir(self) -> Path:
        return self.index_dir / "chroma"

    @property
    def groq_api_key(self) -> str:
        key = os.getenv("GROQ_API_KEY", "").strip()
        if not key:
            raise RuntimeError("Add your GROQ_API_KEY to the project .env file.")
        return key
