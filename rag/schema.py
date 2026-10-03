from dataclasses import dataclass

@dataclass(frozen=True)
class RagAnswer:
    text: str
    sources: list[str]
