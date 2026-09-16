from pathlib import Path
import sys
from langchain_huggingface import HuggingFaceEmbeddings

# Ensure `rag` (the parent folder) is on sys.path so `import config...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_text_splitters import RecursiveCharacterTextSplitter
import config.project_config as config

def load_embedding_model():
    """
    Load the HuggingFace embedding model.
    """

    config.embedding_model = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL
    )

    return config.embedding_model

def generate_embeddings(chunks, batch_size=32):
    """
    Generate embeddings using batch processing.

    Args:
        chunks: List of document chunks.
        batch_size: Number of chunks processed in one batch.

    Returns:
        List of embeddings.
    """

    # Load embedding model
    load_embedding_model()

    config.vectors = []

    # Process chunks in batches
    for i in range(0, len(chunks), batch_size):

        batch = chunks[i:i + batch_size]

        print(
            f"Processing batch: "
            f"{i} - {i + len(batch)}"
        )

        # Extract text from Document objects
        batch_texts = [
            chunk.page_content
            for chunk in batch
        ]

        # Generate embeddings for current batch
        batch_embeddings = config.embedding_model.embed_documents(
            batch_texts
        )

        # Store embeddings
        config.vectors.extend(batch_embeddings)

    return config.vectors