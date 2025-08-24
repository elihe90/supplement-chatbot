# main.py

import os
import traceback
import logging
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# LangChain Imports
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.chat_message_histories import RedisChatMessageHistory

# --- Setup basic logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Load Environment Variables ---
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("AVALAI_BASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
JSON_FILE = "products.json"

if not all([API_KEY, BASE_URL, REDIS_URL]):
    raise ValueError("API key, Base URL, or Redis URL not found. Please check your .env file.")

# --- Global variable to hold the in-memory vector store ---
vector_store_in_memory = None

def build_vector_store_from_json():
    logging.info("Building in-memory vector store from scratch...")
    if not os.path.exists(JSON_FILE):
        raise FileNotFoundError(f"Source JSON file '{JSON_FILE}' not found.")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        products_data = json.load(f)
    all_documents = []
    for product in products_data:
        soup = BeautifulSoup(product.get('description', ''), 'html.parser')
        clean_description = soup.get_text(separator=' ', strip=True)
        content = (
            f"عنوان محصول: {product.get('title', '')}\n"
            f"توضیحات: {clean_description}\n"
            f"فواید: {', '.join(product.get('benefits', []))}\n"
            f"عوارض جانبی احتمالی: {', '.join(product.get('side_effects', []))}"
        )
        if content.strip():
            metadata = {"source": product.get('page_url', 'N/A'), "title": product.get('title', 'N/A')}
            all_documents.append(Document(page_content=content, metadata=metadata))
    custom_headers = {"Authorization": f"Bearer {API_KEY}"}
    embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002", base_url=BASE_URL, default_headers=custom_headers, timeout=60)
    db = Chroma.from_documents(documents=all_documents, embedding=embeddings_model)
    logging.info(f"✅ In-memory vector store created successfully with {len(all_documents)} documents.")
    return db

def get_vector_store():
    global vector_store_in_memory
    if vector_store_in_memory is None:
        vector_store_in_memory = build_vector_store_from_json()
    return vector_store_in_memory

def get_session_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=REDIS_URL, ttl=86400)

# --- Initialize AI Components on App Startup ---
retriever = get_vector_store().as_retriever(search_kwargs={"k": 5})
custom_headers = {"Authorization": f"Bearer {API_KEY}"}
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, base_url=BASE_URL, default_headers=custom_headers, timeout=60)

# --- FastAPI App ---
app = FastAPI(title="Supplement Store AI Advisor with Memory")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Conversational Retrieval Chain ---

# 1. Condenser Prompt: Creates a standalone question from history
condenser_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
    ("ai", "Please rephrase the follow-up question to be a standalone question, in its original language."),
])

# 2. Condenser Chain: Runs the condenser prompt
condenser_chain = condenser_prompt | llm | StrOutputParser()

# 3. RAG Prompt: The main prompt for answering the question
answer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful and friendly AI assistant for the 'Safir Servat' online supplement store. "
     "Answer the user's question based *only* on the provided context. "
     "If the context is insufficient, politely state that you don't have information on that specific topic. "
     "Always provide the product name and a link to its page when recommending a product. "
     "Answer in Persian.\n\nContext:\n{context}"
    ),
    ("human", "{question}"),
])

def format_docs(docs):
    return "\n\n---\n\n".join(
        f"Product Title: {doc.metadata.get('title', '')}\n"
        f"Product Content: {doc.page_content}\n"
        f"Product Page Link (source): {doc.metadata.get('source', '')}"
        for doc in docs
    )

# 4. The main RAG chain for answering questions
rag_chain = (
    RunnablePassthrough.assign(
        context=condenser_chain | retriever | format_docs
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

# 5. Wrap with memory
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
    # The output of the wrapped chain is a string, so we don't need an output key here.
)

# --- API Data Models ---
class ChatInput(BaseModel):
    message: str
    session_id: str

class ChatOutput(BaseModel):
    response: str

# --- API Endpoints ---
@app.post("/chat", response_model=ChatOutput)
async def chat_with_bot(request: ChatInput):
    try:
        config = {"configurable": {"session_id": request.session_id}}
        # The output of this chain is a string because the final step is StrOutputParser()
        response_text = await conversational_rag_chain.ainvoke({"question": request.message}, config=config)
        return ChatOutput(response=response_text)
    except Exception as e:
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))
