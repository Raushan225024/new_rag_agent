from pathlib import Path
import sys

# Ensure `rag` (the parent folder) is on sys.path so `import config...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config.project_config as config
from langchain_community.document_loaders import PyPDFLoader


def load_documents():
    config.document = []

    # Load all PDF files from the data folder
    for pdf_file in config.DATA_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        config.document.extend(loader.load())

    return config.document