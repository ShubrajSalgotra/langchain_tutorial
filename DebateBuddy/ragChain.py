from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def rag_response(question):
    
    embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")
    
    vectorstore = Chroma(persist_directory = "DebateBuddy/vectorStore", embedding_function = embeddings)

    retriever = vectorstore.as_retriever(search_kwargs = {"k" : 3})
    docs = retriever.invoke(question)

    context = "\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a debate coach. The topic is: Democracies ought to prioritize the protection of civil liberties over national security. Only answer the question from the given context. "),
    ("human", "Context: {context} \n\n Question: {question}")])

    model = init_chat_model("google_genai:gemini-3-flash-preview")
    chain = prompt | model
    response = chain.invoke({
        "context" : context, 
        "question" : question
    })
    return response.content