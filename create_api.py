from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import config.project_config as config

from retrival.retriver import retrieve_documents
from llmcall.llmcall import ask_llm
from retrival.question_embed import load_embedding_model
embadding_model = None


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
    global embedding_model

    try:
        # First request पर model load होगा
        if embedding_model is None:
            print("Loading embedding model...")
            embedding_model = load_embedding_model()
            print("Embedding model loaded")
        embadded_question = embedding_model.embed_query(request.question)
        docs = retrieve_documents(embadded_question)
        question = request.question

        

        answer = ask_llm(
            question,
            docs
        )

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as error:
        print("Error:", repr(error))
        
        