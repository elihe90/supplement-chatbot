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
