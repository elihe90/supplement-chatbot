# build_vector_db.py

import os
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
proxy_url = os.getenv("PROXY_URL")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

if not proxy_url:
    raise ValueError("PROXY_URL not found in environment variables.")

# 1. Load product data from the JSON file
try:
    with open("products_1.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        products_data = data.get('products', []) # این خط اصلاح شده است
except FileNotFoundError:
    print("Error: products_1.json file not found.")
    exit()

print(f"Loaded {len(products_data)} products.")

# 2. Prepare Documents for LangChain
documents = []
for p in products_data:
    content = f"محصول: {p.get('title', 'نامشخص')}\n"
    content += f"نام انگلیسی: {p.get('en_title', 'نامشخص')}\n"
    content += f"توضیحات: {p.get('description', 'توضیحات ندارد')}\n"

    # این بخش برای فایل‌های جدیدی که ممکن است ساختار متفاوتی داشته باشند، انعطاف‌پذیرتر است.
    # به جای benefits/side_effects، از fullContent استفاده می‌کنیم اگر وجود داشته باشد.
    if isinstance(p.get('fullContent'), str):
        content += f"توضیحات کامل و FAQ: {p['fullContent']}"
    
    metadata = {
        "title": p.get('title'),
        "page_url": p.get('page_url')
    }

    documents.append(Document(page_content=content, metadata=metadata))

# 3. Define the Embedding Model with the correct base_url
embeddings = OpenAIEmbeddings(api_key=openai_api_key, base_url=proxy_url)

# 4. Create and persist the Vector Store
vector_db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
vector_db.persist()

print("\nVector Database created and persisted successfully in './chroma_db' directory.")
print(f"It contains {vector_db._collection.count()} documents.")