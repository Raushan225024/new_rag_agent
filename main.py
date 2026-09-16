import config.project_config as config
from ingestion.loader import load_documents
from ingestion.chunker import create_chunks
from ingestion.embedder import generate_embeddings
from ingestion.store_vectors import upload_batch_data
load_documents()
print(f"document: {len(config.document)}")
create_chunks()
print(f"chunks:{len(config.chunks)}")
generate_embeddings(config.chunks, batch_size=32)
print(f"vectors:{len(config.vectors)}")
print(f"vectors:{type(config.vectors)}")
print(f"vectors:{type(config.vectors[0])}")
upload_batch_data(config.vectors, batch_size=10)