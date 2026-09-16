from pathlib import Path
import sys

# Ensure `rag` (the parent folder) is on sys.path so `import config...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_text_splitters import RecursiveCharacterTextSplitter
import config.project_config as config


def create_chunks():
    # Check if documents are loaded
    if config.document is None:
        raise ValueError("No document found. Please load the document first.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )

    # Create chunks
    config.chunks = splitter.split_documents(config.document)

    return config.chunks