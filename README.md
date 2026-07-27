# 🚀 ContextIQ

> **Enterprise Retrieval-Augmented Generation (RAG) Chatbot for Organizational Knowledge Management**

ContextIQ is a production-ready AI-powered enterprise chatbot that enables employees to query organizational documents using natural language. It leverages Retrieval-Augmented Generation (RAG) with role-based authentication, department-specific knowledge bases, persistent chat history, document management, and semantic search.

---

## 📌 Features

### 🔐 Authentication & Authorization
- Role-based Login System
- Admin Dashboard
- User Dashboard
- Department-wise Access Control
- Secure User Authentication

### 📚 Knowledge Base Management
- Create Knowledge Bases
- Upload PDF Documents
- Delete Documents
- Delete Knowledge Bases
- Duplicate Document Detection
- Document Registry
- Metadata Management

### 🤖 AI Chatbot
- Retrieval-Augmented Generation (RAG)
- Context-aware Conversations
- Persistent Chat History
- Session Management
- Multi-turn Question Answering
- Source Citations

### 🔎 Semantic Search
- Sentence Transformer Embeddings
- Chroma Vector Database
- Department-wise Document Retrieval
- Top-K Relevant Chunk Retrieval

### 💾 Data Management
- Persistent Vector Database
- JSON-based User Management
- Chat History Storage
- Knowledge Base Registry

---

# 🏗️ Project Architecture

```
User
   │
   ▼
Login Authentication
   │
   ├──────────────┐
   ▼              ▼
Admin         Employee
Dashboard      Dashboard
   │              │
   ▼              ▼
Knowledge Base   Ask Question
Management       │
                 ▼
          Query Reformulation
                 │
                 ▼
          Chroma Retriever
                 │
                 ▼
         Relevant Document Chunks
                 │
                 ▼
              Groq LLM
                 │
                 ▼
          Final Response + Citations
```

---

# 📂 Project Structure

CONTEXTIQ/
│
├── app.py                              # Main Streamlit application
├── admin.py                            # Admin entry point
├── requirements.txt                    # Project dependencies
├── README.md                           # Project documentation
├── .env                                # Environment variables
│
├── data/
│   ├── chat_history/                   # Persistent user chat sessions
│   ├── raw_docs/                       # Uploaded PDF documents organized by Knowledge Base
│   ├── vector_db/                      # ChromaDB vector database
│   ├── users.json                      # User credentials and roles
│   ├── knowledge_bases.json            # Knowledge Base metadata
│   └── document_registry.json          # Uploaded document registry
│
├── src/
│   │
│   ├── assets/
│   │   └── login_illustration.jpg      # Login page illustration
│   │
│   ├── auth/
│   │   ├── auth_manager.py             # User authentication and authorization
│   │   └── login.py                    # Login interface
│   │
│   ├── chains/
│   │   └── rag_chain.py                # RAG pipeline orchestration
│   │
│   ├── ingestion/
│   │   ├── embeddings.py               # Embedding generation
│   │   ├── pdf_loader.py               # PDF loading and text extraction
│   │   └── splitter.py                 # Semantic text chunking
│   │
│   ├── knowledge_base/
│   │   ├── delete.py                   # Document deletion
│   │   ├── duplicate.py                # Duplicate document detection
│   │   ├── ingestion_manager.py        # End-to-end document ingestion
│   │   ├── kb_manager.py               # Knowledge Base management
│   │   ├── metadata.py                 # Metadata extraction
│   │   └── registry.py                 # Document registry management
│   │
│   ├── llm/
│   │   └── groq_client.py              # Groq LLM configuration
│   │
│   ├── memory/
│   │   ├── chat_history.py             # Chat history management
│   │   └── session_manager.py          # Session management
│   │
│   ├── prompts/
│   │   └── prompts.py                  # System prompts
│   │
│   ├── retrieval/
│   │   └── retriever.py                # ChromaDB retriever
│   │
│   ├── services/
│   │   ├── admin_service.py            # Admin business logic
│   │   └── rag_service.py              # Query processing service
│   │
│   ├── ui/
│   │   ├── admin_dashboard.py          # Admin dashboard
│   │   └── user_dashboard.py           # User dashboard
│   │
│   └── vectordb/
│       └── chroma_store.py             # ChromaDB operations

```
---


# ⚙️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### LLM
- Groq API (Llama 3)

### Frameworks
- LangChain

### Embedding Model
- all-MiniLM-L6-v2

### Vector Database
- ChromaDB

### Document Loader
- PyPDF

### Storage
- JSON
- Local File System

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/contextiq.git

cd contextiq
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---

# 👤 User Roles

## Admin

Admin can

- Create Knowledge Bases
- Delete Knowledge Bases
- Upload PDFs
- Delete PDFs
- Manage Documents
- View Registered Documents

---

## User

Users can

- Login
- Access department-specific knowledge base
- Ask questions
- View chat history
- Receive cited responses

---

# 📚 RAG Pipeline

```
PDF Upload

      │

      ▼

Document Loader

      │

      ▼

Text Splitter

      │

      ▼

Embedding Model

      │

      ▼

Chroma Vector Database

      │

      ▼

Retriever

      │

      ▼

Prompt Template

      │

      ▼

Groq LLM

      │

      ▼

Final Answer + Citations
```

---

# 📊 Current Features

✅ Role-Based Authentication

✅ Knowledge Base Management

✅ Department-wise Access

✅ PDF Upload

✅ Duplicate Detection

✅ Metadata Extraction

✅ Chroma Vector Database

✅ Semantic Search

✅ Persistent Chat History

✅ Source Citations

✅ Admin Dashboard

✅ User Dashboard

---

# 🔮 Future Improvements

- Multi-format Document Support (DOCX, PPTX)
- Hybrid Search (Keyword + Semantic)
- User Feedback System
- Response Streaming
- Cloud Deployment
- Audit Logs
- Analytics Dashboard
- OCR Support for Scanned PDFs

---

# 📜 License

This project is developed for educational and internship purposes.

---

# 👩‍💻 Developer

**Akshita Saxena**

B.Tech Electronics & Computer Engineering

AI • Machine Learning • Computer Vision • Generative AI