from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import snapshot_download
from huggingface_hub.errors import LocalEntryNotFoundError

class Embedder:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def create(self) -> HuggingFaceEmbeddings:
        try:
            model = snapshot_download(self.model_name, local_files_only=True)
        except LocalEntryNotFoundError:
            model = self.model_name

        return HuggingFaceEmbeddings(
            model_name=model,
        )
