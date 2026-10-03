from dataclasses import dataclass

@dataclass(frozen=True)
class Measurement:
    indicator: str
    geography: str
    year: int
    dimension: str
    value: float
    displayed: str
    comment: str
    source: str
    sheet: str
    row: int

@dataclass(frozen=True)
class RagAnswer:
    text: str
    sources: list[str]
    