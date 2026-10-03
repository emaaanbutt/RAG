from langchain_huggingface import HuggingFaceEmbeddings

class Embedder:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def create(self) -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(
            model_name = self.model_name
        )
        