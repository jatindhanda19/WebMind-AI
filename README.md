🌐 WebMind AI — Chat with Any Website

💬 Transform any website into an interactive AI assistant using Retrieval-Augmented Generation (RAG).

WebMind AI is an end-to-end Generative AI application that allows users to chat with the content of any public website. It extracts webpage data, builds a semantic vector index, retrieves relevant context, and generates grounded answers using a Large Language Model.

🎥 Demo Video

👉 Watch the project demo:
(https://github.com/user-attachments/assets/f9107eda-4902-4aa6-a798-83c4ca39e10b)

🚀 Features
Feature	Description
🌐 Website Input	Enter any public website URL
🔍 RAG Pipeline	Retrieves relevant content from the webpage
💬 Conversational Chat	Ask follow-up questions naturally
🧠 Context-Aware Answers	Responses grounded in website content
⚡ Fast Inference	Powered by Groq LLM
🗄️ Local Vector Store	No external database required
🔄 Switch Websites	Load and analyze new URLs anytime
🧠 System Architecture
User Enters URL
        │
        ▼
Website Loader
        │
        ▼
Text Cleaning & Chunking
        │
        ▼
Embeddings (MiniLM)
        │
        ▼
Vector Database (FAISS)
        │
        ▼
Retriever (Similarity Search)
        │
        ▼
LLM → Context-Aware Answer
        │
        ▼
💬 Chat Interface
⚙️ Tech Stack
🤖 AI / NLP

LangChain — RAG orchestration

Groq LLM — Fast inference (LLaMA-3)

HuggingFace Embeddings — Sentence embeddings

Retrieval-Augmented Generation (RAG)

🗄️ Vector Database

FAISS — Local semantic search

🌐 Data Processing

WebBaseLoader — Website scraping

RecursiveCharacterTextSplitter — Text chunking

🖥️ Frontend

Streamlit — Interactive web interface

🐍 Backend

Python

📂 Project Structure
WebMind-AI/
│
├── app.py              # Streamlit application interface
├── rag_engine.py       # Website loading, chunking, embeddings & FAISS
├── langgraph_flow.py   # RAG workflow (if used)
├── evaluation.py       # RAG evaluation (optional)
├── requirements.txt    # Dependencies
└── README.md
🔄 Pipeline Workflow
1️⃣ Website Processing

The provided URL is loaded and cleaned to extract meaningful textual content.

2️⃣ Text Chunking

Large text is split into smaller overlapping chunks for better retrieval.

3️⃣ Embedding Generation

Each chunk is converted into vector embeddings using a HuggingFace model.

4️⃣ Vector Storage

Embeddings are stored in a FAISS vector database for fast similarity search.

5️⃣ Retrieval-Augmented Generation (RAG)

When a question is asked:

Relevant chunks are retrieved

Context is injected into the prompt

The LLM generates a grounded response

6️⃣ Conversational Output

The AI answers questions based only on the website content, enabling accurate and contextual interactions.

💬 Example Interaction
User: What is the main topic of this website?

AI: This website focuses on artificial intelligence,
    including machine learning, deep learning,
    and real-world AI applications.

User: Can you explain machine learning?

AI: Machine learning is a subset of AI that enables
    systems to learn patterns from data and make
    predictions without explicit programming.
🖥️ Getting Started
1️⃣ Clone the Repository
git clone https://github.com/yourusername/webmind-ai.git
cd webmind-ai
2️⃣ Create Virtual Environment
python -m venv .venv

Activate:

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Add API Key

Create a .env file:

GROQ_API_KEY=your_api_key_here
5️⃣ Run the Application
streamlit run app.py

Open the local URL shown in your terminal (usually http://localhost:8501
).

⚠️ Limitations

Works only with publicly accessible websites

Some JavaScript-heavy pages may not load correctly

Only analyzes the provided page (not the entire domain)

🔮 Future Improvements

Multi-page website crawling

Source citations in answers

Document upload support (PDF, DOCX)

Persistent knowledge base

Cloud deployment

📊 RAG Evaluation (Optional)

Evaluation can be performed using RAGAS metrics to measure faithfulness and relevance of generated answers.

⚠️ Deployment Status

The project currently runs locally.
Deployment on cloud platforms may require configuration adjustments for API keys and dependencies.

👨‍💻 Author

Jatin Dhanda
AI / Machine Learning Enthusiast — focused on building LLM-powered intelligent systems 🚀





