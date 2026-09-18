import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
)

prompt = ChatPromptTemplate.from_template(
    """
You are an AI assistant representing Raushan Kumar.

The user is asking questions about Raushan Kumar.

IMPORTANT:
When the user says "you", "your", or "yourself",
interpret it as referring to Raushan Kumar.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}


Answer:
"""
)


def ask_llm(question, docs):

    context = "\n\n".join(
        doc["content"] for doc in docs
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return response.content