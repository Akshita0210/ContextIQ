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

```text
CONTEXTIQ/
│
├── app.py
├── admin.py
├── requirements.txt
├── README.md
├── .env
│
├── data/
│   ├── chat_history/
│   ├── raw_docs/
│   ├── vector_db/
│   ├── users.json
│   ├── knowledge_bases.json
│   └── document_registry.json
│
├── src/
│   ├── assets/
│   │   └── login_illustration.jpg
│   │
│   ├── auth/
│   │   ├── auth_manager.py
│   │   └── login.py
│   │
│   ├── chains/
│   │   └── rag_chain.py
│   │
│   ├── ingestion/
│   │   ├── embeddings.py
│   │   ├── pdf_loader.py
│   │   └── splitter.py
│   │
│   ├── knowledge_base/
│   │   ├── delete.py
│   │   ├── duplicate.py
│   │   ├── ingestion_manager.py
│   │   ├── kb_manager.py
│   │   ├── metadata.py
│   │   └── registry.py
│   │
│   ├── llm/
│   │   └── groq_client.py
│   │
│   ├── memory/
│   │   ├── chat_history.py
│   │   └── session_manager.py
│   │
│   ├── prompts/
│   │   └── prompts.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── services/
│   │   ├── admin_service.py
│   │   └── rag_service.py
│   │
│   ├── ui/
│   │   ├── admin_dashboard.py
│   │   └── user_dashboard.py
│   │
│   └── vectordb/
│       └── chroma_store.py
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