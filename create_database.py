# create_database.py

import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

# Load environment variables from the .env file
load_dotenv()

# --- Configuration ---
JSON_FILE_PATH = 'products_1.json'
PERSIST_DIRECTORY = 'chroma_db'
EMBEDDING_MODEL = "text-embedding-ada-002"

def load_and_clean_data(file_path):
    """
    Reads the JSON file, cleans HTML from descriptions,
    and prepares the data in LangChain's Document format, skipping empty ones.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

    documents = []
    for product in products:
        soup = BeautifulSoup(product.get('description', ''), 'html.parser')
        clean_description = soup.get_text(separator=' ', strip=True)

        page_content = (
            f"Product Title: {product.get('title', '')}\n"
            f"Description: {clean_description}\n"
            f"Benefits: {', '.join(product.get('benefits', []))}\n"
            f"Potential Side Effects: {', '.join(product.get('side_effects', []))}"
        )
        
        # --- FINAL FIX ---
        # Check if the generated content is not empty or just whitespace.
        if page_content.strip():
            metadata = {
                "source": product.get('page_url', ''),
                "title": product.get('title', '')
            }
            documents.append(Document(page_content=page_content, metadata=metadata))
        else:
            # Optional: Log which product is being skipped
            print(f"--> Skipping product with empty content: {product.get('title', 'Untitled')}")
        # --- END OF FINAL FIX ---

    return documents

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("AVALAI_BASE_URL")

    if not api_key or not base_url:
        print("Error: Ensure OPENAI_API_KEY and AVALAI_BASE_URL are set in the .env file.")
        return

    print("Step 1: Loading and cleaning product data...")
    documents = load_and_clean_data(JSON_FILE_PATH)
    if not documents:
        print("No documents were loaded. Exiting.")
        return
    print(f"Successfully processed {len(documents)} products.")

    print("\nStep 2: Creating embeddings and building the ChromaDB vector store...")
    
    # Using the standard "Authorization" header which your test proved is correct.
    custom_headers = {"Authorization": f"Bearer {api_key}"}
    
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=base_url,
        default_headers=custom_headers
    )

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    print(f"\nSuccess! The knowledge base has been created and saved in the '{PERSIST_DIRECTORY}' directory.")

if __name__ == "__main__":
    main()