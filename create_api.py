from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import config.project_config as config

from retrival.retriver import retrieve_documents
from llmcall.llmcall import ask_llm
from retrival.text_embed_api import text_to_vector


# ---------------------------------
# Load Embedding Model
# ---------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading embedding model...")

    #load_embedding_model()

    print("Embedding model loaded successfully")

    yield

    print("Shutting down application...")


# ---------------------------------
# Create FastAPI App
# ---------------------------------

app = FastAPI(
    title="RAG Chat API",
    description="Semantic Search + LLM",
    version="1.0.0",
    lifespan=lifespan
)

#-------------------------------
# add middleware to allow CORS
#-------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------------------
# Request Schema
# ---------------------------------

class QuestionRequest(BaseModel):

    question: str


# ---------------------------------
# Root Endpoint
# ---------------------------------

@app.get("/")
def home():

    return {
        "message": "RAG Chat API is running"
    }


# ---------------------------------
# Ask Endpoint
# ---------------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):
    

    try:
        print("\n========== ASK REQUEST ==========")
        print("Question:", request.question)

        # 1. Load embedding model
        

        # 2. Generate question embedding
        print("Generating question embedding...")

        embedded_question = text_to_vector(
            request.question
        )

        print(
            "Embedding generated. Length:",
            len(embedded_question)
        )

        # 3. Retrieve documents from Supabase
        print("Retrieving documents from Supabase...")

        docs = retrieve_documents(embedded_question)

        print("Retrieved documents:")
        print(docs)

        # Check retrieved documents
        if not docs:
            print("No documents retrieved")

            return {
                "question": request.question,
                "answer": "No relevant documents found."
            }

        # 4. Call LLM
        print("Calling LLM...")

        answer = ask_llm(
            request.question,
            docs
        )

        print("LLM answer:")
        print(answer)

        # 5. Return response
        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as error:

        print("ERROR OCCURRED:", repr(error))

        return {
            "error": str(error)
        }