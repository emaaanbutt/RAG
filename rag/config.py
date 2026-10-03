from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    root: Path = Path(__file__).resolve().parents[1]

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    answer_model: str = "Qwen/Qwen2.5-1.5B-Instruct"
    vision_model: str = "HuggingFaceTB/SmolVLM-256M-Instruct"

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
    def evidence_path(self) -> Path:
        return self.index_dir / "evidence.jsonl"

    @property
    def numeric_path(self) -> Path:
        return self.index_dir / "measurements.sqlite"

    