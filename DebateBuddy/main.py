from dotenv import load_dotenv
from ragChain import rag_response

load_dotenv()

question = input("Type your question: ")
answer = rag_response(question)
print(answer["text"])