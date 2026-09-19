import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)


def text_to_vector(text: str) -> list[float]:
    """
    Convert query text into a 384-dimensional embedding vector
    using sentence-transformers/all-MiniLM-L6-v2.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    embedding = client.feature_extraction(
        text,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Convert numpy array / tensor-like result to Python list
    vector = embedding.tolist()

    # Verify dimension
    if len(vector) != 384:
        raise ValueError(
            f"Expected 384 dimensions, got {len(vector)}"
        )

    return vector