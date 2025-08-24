# debug_avalai.py
import os
import json
import requests
from dotenv import load_dotenv

# --- SCRIPT SETUP ---
# This script will help us find the exact cause of the 400 error.
# It makes a direct request to the AvalAI proxy without using LangChain.

# Load credentials from your .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("AVALAI_BASE_URL")

# --- VERIFICATION ---
# Verify that the credentials have been loaded correctly
print("--- Verifying Credentials ---")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file.")
    exit()
print(f"✅ API Key loaded (last 4 chars): ...{api_key[-4:]}")

if not base_url:
    print("❌ ERROR: AVALAI_BASE_URL not found in .env file.")
    exit()
print(f"✅ Base URL loaded: {base_url}")
print("-" * 30)

# --- REQUEST DETAILS ---
# The specific endpoint for creating embeddings
# Ensure your base_url ends with '/v1'
embedding_url = f"{base_url.rstrip('/')}/embeddings"

# The data we are trying to send (the 'input')
payload = {
    "input": "This is a simple test sentence to create an embedding.",
    "model": "text-embedding-ada-002"
}

# The headers for authentication (the 'token')
# We will use the standard "Authorization" header format that your previous test confirmed.
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# --- SENDING THE REQUEST ---
print("\n--- Sending Request ---")
print(f"URL: {embedding_url}")
print(f"Headers: {headers}")
print(f"Payload: {json.dumps(payload)}")
print("-" * 30)

try:
    # Make the POST request to the server
    response = requests.post(embedding_url, headers=headers, json=payload)
    
    # --- ANALYZING THE RESPONSE ---
    print("\n--- Received Response ---")
    print(f"Status Code: {response.status_code}")
    
    # Try to print the JSON response, or the raw text if it's not JSON
    try:
        print(f"Response Body (JSON): {response.json()}")
    except json.JSONDecodeError:
        print(f"Response Body (Text): {response.text}")
    print("-" * 30)

except requests.exceptions.RequestException as e:
    print("\n--- REQUEST FAILED ---")
    print(f"A connection error occurred: {e}")
    print("Please check if your AVALAI_BASE_URL is correct and the server is reachable.")
    print("-" * 30)