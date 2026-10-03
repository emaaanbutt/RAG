from io import BytesIO

class VisionReader:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.pipe = None

    def describe(self, png_bytes: bytes) -> str:
        from PIL import Image
        from transformers import pipeline

        if self.pipe is None:
            self.pipe = pipeline(
                "image-text-to-text",
                model=self.model_name
            )

        image = Image.open(BytesIO(png_bytes)).convert("RGB")

        messages = [{
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": (
                    "Describe charts, diagrams, and important labels. "
                    "If a word or value is unreadable, say so. Do not guess numbers."
                )},
            ],
        }]

        output =  self.pipe(
            text= messages,
            max_new_tokens = 300,
            return_full_text = False
        )

        generated = output[0]["generated_text"]

        if isinstance(generated, list):
            generated = generated[-1]["content"]

        return str(generated).strip()
