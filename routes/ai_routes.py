from flask import Blueprint, request, jsonify
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
import sqlite3

# Load .env for OpenAI key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

ai_bp = Blueprint('ai', __name__)

# 🔁 Simple SQLite cache
def cache_response(prompt, response=None):
    conn = sqlite3.connect("cache.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS cache (prompt TEXT PRIMARY KEY, response TEXT)")
    
    if response:
        cur.execute("INSERT OR REPLACE INTO cache (prompt, response) VALUES (?, ?)", (prompt, response))
        conn.commit()
        conn.close()
        return
    else:
        cur.execute("SELECT response FROM cache WHERE prompt = ?", (prompt,))
        result = cur.fetchone()
        conn.close()
        return result[0] if result else None

# 🧠 Load RAG components
embeddings = OpenAIEmbeddings(api_key=openai_api_key)
db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(api_key=openai_api_key), retriever=db.as_retriever())

# 📡 API route
@ai_bp.route('/api/ask', methods=['POST'])
def ask():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    # Check cache first
    cached = cache_response(prompt)
    if cached:
        return jsonify({'response': cached})

    # Run through RAG system
    try:
        answer = qa_chain.run(prompt)
        cache_response(prompt, answer)
        return jsonify({'response': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
