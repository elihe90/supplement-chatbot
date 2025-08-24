# Smart Supplement Chatbot Advisor

This project is an intelligent, AI-powered chatbot designed to act as a virtual assistant for a dietary supplement e-commerce website.The primary goal of the chatbot is to provide accurate and personalized advice to customers regarding product selection, comparison, and usage instructions. By using this tool, customers can quickly access the information they need and have a better shopping experience. Intelligent Product Consultation: The chatbot can answer user questions based on their specific needs, such as fitness goals, health concerns, or skin problems.

####  Product Comparison: 
   It can compare two or more similar products and provide key information to help customers make an informed decision.

#### 
   FAQ Answering: It is capable of responding to common questions about products, usage methods, potential side effects, and precautions.

####  Conversation Memory:
   The chatbot uses Redis to store conversation history, allowing it to provide coherent and continuous responses throughout a single chat     session.

### Accurate Response Generation with RAG: 
 It utilizes a Retrieval-Augmented Generation (RAG) architecture to ensure that its answers are based exclusively on your provided knowledge base (the products.json     file), preventing it from using general knowledge from the language model.

### Simple User Interface: 
  The user interface is a clean and user-friendly web chat window built with HTML, CSS, and JavaScript for seamless customer interaction.

## Technologies Used
Programming Language: Python

Backend Framework: FastAPI

AI Libraries: LangChain, langchain-openai, langchain-chroma

Language Model (LLM): ChatGPT (via OpenAI API)

Vector Database: ChromaDB (for storing product information)

Memory Database: Redis (for storing chat history)

API Proxy: Avala AI (for API access)

Frontend: HTML, CSS, JavaScript

## Setup and Installation
### Prerequisites
To run this project, you will need the following tools and services:

Python 3.9+

Docker (for setting up Redis)

An API key from OpenAI and access to the Avala AI proxy

### Installation Steps
Clone the repository:
Start by cloning the project from its GitHub repository to your local machine.

#### git clone https://github.com/YourUsername/supplement-chatbot.git

Navigate to the project folder:

Move into the newly created project directory.
cd supplement-chatbot

Create and activate a virtual environment:

Set up a virtual environment to manage project dependencies and activate it.
#### python -m venv .venv
#### source .venv/bin/activate
Install the required packages:
Install all the necessary Python libraries listed in the requirements.txt file.
####  pip install -r requirements.txt
Create and configure the .env file:
Create a .env file and add your credentials. Make sure to replace the placeholder values with your actual keys and URLs.

OPENAI_API_KEY="your_openai_api_key_here"
AVALAI_BASE_URL="https://proxy.avala.ai/v1"
REDIS_URL="redis://localhost:6379/0"
Run the Redis database with Docker:
Use Docker to start a Redis container, which your chatbot will use for conversation memory.
#### docker run --name my-redis -p 6379:6379 -d redis
Start the backend server:
Launch the FastAPI server. This command will also automatically build the vector database from your products_1.json file.
#### uvicorn main:app --reload
Open the frontend:
###  Author
