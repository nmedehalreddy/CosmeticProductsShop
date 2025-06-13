from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os

def ingest():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Read raw FAQ file
    with open("data/faq.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk) for chunk in text_splitter.split_text(text)]

    # Create embedding + FAISS index
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    db = FAISS.from_documents(docs, embeddings)

    # Save index to local folder
    db.save_local("vectorstore")
    print("✅ FAQ data indexed successfully!")

if __name__ == "__main__":
    ingest()
