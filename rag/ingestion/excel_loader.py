from pathlib import Path

from langchain_core.documents import Document
from openpyxl import load_workbook


class ExcelLoader:
    def __init__(self, project_root: Path):
        self.project_root = project_root

    def load(self, path: Path) -> list[Document]:
        source = str(path.relative_to(self.project_root))
        documents = []
        workbook = load_workbook(path, read_only=True, data_only=True)

        try:
            for sheet in workbook:
                rows = sheet.iter_rows(values_only=True)
                first_row = next(rows, None)
                if first_row is None:
                    continue

                if sheet.max_row == 1:
                    note = " | ".join(str(value) for value in first_row if value is not None)
                    documents.append(Document(
                        page_content=note,
                        metadata={"source": source, "sheet": sheet.title, "row": 1, "kind": "xlsx_note"},
                    ))
                    continue

                headers = [
                    str(value).strip() if value is not None else f"column_{i}"
                    for i, value in enumerate(first_row, start=1)
                ]

                for row_number, values in enumerate(rows, start=2):
                    fields = [
                        f"{header}: {value}"
                        for header, value in zip(headers, values)
                        if value is not None and str(value).strip()
                    ]
                    if fields:
                        documents.append(Document(
                            page_content=" | ".join(fields),
                            metadata={
                                "source": source,
                                "sheet": sheet.title,
                                "row": row_number,
                                "kind": "xlsx_row",
                            },
                        ))
        finally:
            workbook.close()

        return documents
