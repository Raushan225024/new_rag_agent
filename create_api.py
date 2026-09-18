from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import config.project_config as config

from retrival.retriver import retrieve_documents
from llmcall.llmcall import ask_llm
from retrival.question_embed import load_embedding_model


# ---------------------------------
# Load Embedding Model
# ---------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading embedding model...")

    load_embedding_model()

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

    question = request.question.strip()

    if not question:

        return {
            "error": "Question cannot be empty"
        }


    # Get embedding model

    model = config.embedding_model

    print(f"Model: {model}")


    # Convert question into embedding

    embedded_question = model.embed_query(question)


    # Retrieve documents from Supabase

    docs = retrieve_documents(embedded_question)


    # Send question + documents to LLM

    answer = ask_llm(question, docs)


    # Return response

    return {

        "question": question,

        "answer": answer

    }