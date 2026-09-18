import config.project_config as config
from retrival.retriver import retrieve_documents
from llmcall.llmcall import ask_llm
from retrival.question_embed import load_embedding_model
load_embedding_model()



print("=" * 60)
print("RAG Chat")
print("Type 'exit' to quit")
print("=" * 60)

while True:

    question = input("\nYou : ")

    if question.lower() == "exit":
        break
    model=config.embedding_model
    print(f"model:{model}")
    embadded_question = model.embed_query(question)
    docs = retrieve_documents(embadded_question)

    answer = ask_llm(question, docs)

    print("\nAssistant:")
    print(answer)