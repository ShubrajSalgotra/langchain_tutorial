from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def create_vectorStore():
    loader = PyPDFDirectoryLoader("DebateBuddy/data/documents")
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 100)
    chunks = splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")

    vectorstore = Chroma.from_documents(documents = documents, embedding = embeddings, persist_directory = "DebateBuddy/vectorStore")

    print("VectorDB created ", len(chunks), "chunks")

if __name__ == "__main__":
    create_vectorStore()