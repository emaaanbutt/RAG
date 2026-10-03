from pathlib import Path

import pymupdf
from langchain_core.documents import Document

from rag.ingestion.vision_reader import VisionReader

class PdfLoader:
    def __init__(self, project_root: Path, vision_reader: VisionReader | None = None):
        self.project_root = project_root
        self.vision_reader = vision_reader

    def load(self, path: Path) -> list[Document]:
        source = str(path.relative_to(self.project_root))
        documents = []

        with pymupdf.open(path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                location = {
                    "source": source,
                    "page": page_number
                }

                text = page.get_text("text", sort=True).strip()

                if text:
                    documents.append(Document(
                        page_content=text,
                        metadata={
                            **location,
                            "kind": "pdf_text"
                        },
                    ))

                for table_number, table in enumerate(page.find_tables(), start=1):
                    rows = table.extract()
                    lines = ["|".join(str(cell or "").strip() for cell in row) for row in rows]

                    table_text = "\n".join(lines).strip()

                    if table_text:
                        documents.append(Document(
                            page_content=(
                                f"Table {table_number} on PDF page"
                                f"{page_number}\n{table_number}"
                            ),
                            metadata={
                                **location,
                                "kind": "pdf_table",
                                "table": table_number
                            },
                        ))

                    if self.vision_reader is not None:
                        pixels  = page.get_pixmap(
                            matrix= pymupdf.Matrix(2,2),
                            alpha= False
                        )

                        description = self.vision_reader.describe(
                            pixels.tobytes("png")
                        )

                        if description:
                            documents.append(Document(
                                page_content=description,
                                metadata={
                                    **location,
                                    "kind": "visual_description"
                                },
                            ))

        return documents
