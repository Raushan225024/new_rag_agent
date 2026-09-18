from pathlib import Path
import sys
from langchain_huggingface import HuggingFaceEmbeddings

# Ensure `rag` (the parent folder) is on sys.path so `import config...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

#from langchain_text_splitters import RecursiveCharacterTextSplitter
import config.project_config as config

def load_embedding_model():
    """
    Load the HuggingFace embedding model.
    """

    config.embedding_model = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL
    )

    return config.embedding_model