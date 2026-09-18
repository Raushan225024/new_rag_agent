from pathlib import Path
import sys
import logging


# Add parent directory to sys.path
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from config.vector_db_config import connect_supabase


# -----------------------------
# Logging Configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def retrieve_documents(
    query_embedding,
    k=5
):

    try:

        # Connect to Supabase
        supabase = connect_supabase()

        # Call Supabase RPC function
        response = supabase.rpc(
            "match_document_vector",
            {
                "query_embedding": query_embedding,
                "match_count": k
            }
        ).execute()

        # Get retrieved documents
        documents = response.data
        print(f"Retrieved {len(documents)} documents")
        print(f"type of documents: {type(documents)}")
        print(f"documents: {documents}")
        logging.info(
            f"Retrieved {len(documents)} documents"
        )

        return documents

    except Exception as e:

        logging.error(
            f"Error during retrieval: {e}"
        )

        raise