"""## ⚠️ Disclaimer

This repository includes a **document ingestion pipeline** for processing user-provided documents, generating embeddings, and uploading them to a vector database.

If you want to use the **ingestion pipeline** to upload your own documents to the vector database, please install the following dependencies:

```bash
uv add sentence-transformers langchain-community
```

These dependencies are required because the ingestion pipeline uses **local document processing and embedding generation**.

If you are using only the **RAG API/backend for querying the existing vector database**, these packages may not be required, depending on your configuration.

### Important

* The ingestion pipeline may require additional dependencies depending on the document formats you want to process.
* Make sure your embedding model is compatible with the embedding dimension of your vector database.
* For `sentence-transformers/all-MiniLM-L6-v2`, the embedding dimension is **384**.
* Keep your API keys, database credentials, and other secrets in environment variables. Do not commit them to the repository.

> **Note:** The ingestion pipeline and the production API can use different dependency sets. The API can use a hosted embedding API, while the ingestion pipeline can generate embeddings locally.
"""