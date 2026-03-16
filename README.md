# 🧠 WebMind AI — Chat with Any Website

> An AI-powered conversational assistant that lets you ask questions, extract insights, and explore any website in real time — powered by LangChain, Groq, FAISS, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.43.0-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.2.0-1C3C3C?style=flat)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-F55036?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

##🌐 Live Demo
**🎥 Watch Demo Video:** https://github.com/user-attachments/assets/f4abdb4b-6d73-4748-ac6a-a6577c9c96c4

https://github.com/user-attachments/assets/752cfa12-f1c2-4760-b1b3-1e3359bc10d8

 (Add demo video link)
---

## 📌 Overview

**WebMind AI** is a Retrieval-Augmented Generation (RAG) application that scrapes any publicly accessible website, indexes its content into a FAISS vector store, and enables multi-turn conversational Q&A over that content — all without leaving your browser.

Paste a URL → Ask anything → Get grounded, context-aware answers.

---

## ✨ Features

- 🔗 **Live website ingestion** — scrapes and indexes any public URL on demand
- 🧠 **Conversational memory** — maintains full chat history across turns
- 🔍 **History-aware retrieval** — rewrites search queries based on conversation context
- 🚫 **Grounded answers only** — explicitly refuses to hallucinate outside page content
- ⚡ **Groq-powered inference** — ultra-fast LLaMA 3 responses via Groq API
- 💾 **FAISS vector store** — efficient local similarity search, no external DB needed
- 🔄 **URL hot-swap** — load a new site mid-session without restarting
- 🗑️ **Clear chat** — reset conversation while keeping the loaded site

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User (Browser)                       │
└───────────────────────────┬─────────────────────────────────┘
                            │ enters URL + question
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│         Sidebar (URL input) │ Chat Interface                 │
└──────────────┬──────────────┴──────────────────────────────┘
               │
     ┌─────────▼──────────┐
     │   Ingestion Layer   │
     │  WebBaseLoader      │  ← BeautifulSoup4 + lxml
     │  (scrapes website)  │
     └─────────┬───────────┘
               │ raw documents
     ┌─────────▼───────────┐
     │   Chunking Layer     │
     │  RecursiveCharacter  │  ← chunk_size=1000, overlap=100
     │  TextSplitter        │
     └─────────┬────────────┘
               │ text chunks
     ┌─────────▼───────────┐
     │   Embedding Layer    │
     │  HuggingFaceEmbeddings│ ← all-MiniLM-L6-v2 (local)
     └─────────┬────────────┘
               │ vectors
     ┌─────────▼───────────┐
     │   Vector Store       │
     │   FAISS (in-memory)  │  ← similarity_search(k=3)
     └─────────┬────────────┘
               │ relevant chunks
     ┌─────────▼───────────────────────────────┐
     │         RAG Pipeline (LangChain)         │
     │                                          │
     │  ┌──────────────────────────────────┐   │
     │  │  History-Aware Retriever Chain   │   │
     │  │  (rewrites query using history)  │   │
     │  └──────────────┬───────────────────┘   │
     │                 │                        │
     │  ┌──────────────▼───────────────────┐   │
     │  │  Conversational RAG Chain        │   │
     │  │  (stuffs docs into LLM prompt)   │   │
     │  └──────────────┬───────────────────┘   │
     └─────────────────┼────────────────────────┘
                       │ prompt + context
     ┌─────────────────▼───────────────────┐
     │         Groq API (LLaMA 3 8B)        │
     │     ultra-fast cloud inference       │
     └─────────────────────────────────────┘
```

---

## 🔄 RAG Pipeline — Step by Step

| Step | Component | Description |
|------|-----------|-------------|
| 1 | `WebBaseLoader` | Fetches and parses raw HTML from the given URL |
| 2 | `RecursiveCharacterTextSplitter` | Splits content into 1000-char chunks with 100-char overlap |
| 3 | `HuggingFaceEmbeddings` | Converts chunks to vectors using `all-MiniLM-L6-v2` locally |
| 4 | `FAISS` | Stores vectors in-memory for fast similarity search |
| 5 | `History-Aware Retriever` | Uses LLaMA 3 to rewrite the user query based on prior chat turns |
| 6 | `Stuffed Documents Chain` | Injects top-k retrieved chunks into the LLM system prompt |
| 7 | `ChatGroq (LLaMA 3 8B)` | Generates a grounded answer using only the retrieved context |

---

## 📁 Project Structure

```
webmind-ai/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Pinned dependencies
├── .env                    # API keys (not committed)
├── .env.example            # Template for environment variables
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10 or higher
- A [Groq API key](https://console.groq.com) (free tier available)
- Windows users: [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) installed

### 1. Clone the repository

```bash
git clone https://github.com/your-username/webmind-ai.git
cd webmind-ai
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

> ⚠️ **Windows users only** — install CPU-only PyTorch first to avoid DLL errors:
> ```bash
> pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
> ```

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Usage

1. Paste any public website URL in the **sidebar** (e.g. `https://en.wikipedia.org/wiki/LangChain`)
2. Wait for the ✅ success message — the site is now indexed
3. Type your question in the chat box
4. Ask follow-up questions — the assistant remembers context across turns
5. Paste a new URL anytime to switch websites; chat resets automatically
6. Use **🗑️ Clear chat** to start a fresh conversation on the same site

---

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | API key from [console.groq.com](https://console.groq.com) |

---

## 📦 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | 1.43.0 | Web UI framework |
| `langchain` | 1.2.0 | RAG orchestration |
| `langchain-community` | 0.4.1 | WebBaseLoader, FAISS, HuggingFaceEmbeddings |
| `langchain-groq` | 1.1.2 | Groq LLM integration |
| `faiss-cpu` | 1.8.0 | Local vector similarity search |
| `sentence-transformers` | 3.0.1 | Local embedding model |
| `beautifulsoup4` | 4.12.3 | HTML parsing |
| `python-dotenv` | 1.0.1 | Environment variable loading |

---

## ⚠️ Known Limitations

- **JavaScript-rendered sites** (SPAs, React apps) may return empty content — WebBaseLoader only fetches static HTML
- **Paywalled or login-protected pages** cannot be scraped
- **Very large websites** — only the content on the single URL provided is indexed, not linked pages
- **Rate limits** — Groq free tier has per-minute token limits; high-volume use may require a paid plan

---

## 🛣️ Roadmap

- [ ] Multi-URL ingestion (crawl linked pages)
- [ ] Persistent vector store (save/reload indexed sites)
- [ ] Source citation with page highlights
- [ ] Support for PDF and document uploads
- [ ] Streaming LLM responses
- [ ] Docker deployment support

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add your feature"
git push origin feature/your-feature-name
# Open a Pull Request
```

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) — RAG framework
- [Groq](https://groq.com) — LLM inference API
- [FAISS](https://github.com/facebookresearch/faiss) — Vector similarity search by Meta
- [Sentence Transformers](https://www.sbert.net/) — Local embedding models
- [Streamlit](https://streamlit.io) — Python web app framework
