# rag-chatbot
# Multi-PDF RAG Assistant

A full-stack Retrieval-Augmented Generation (RAG) application that enables users to upload, manage, search, compare, and chat with multiple PDF documents using AI. The system combines semantic search, document retrieval, reranking, and Google Gemini to generate accurate, context-aware responses with source citations.

This project was built to go beyond a basic PDF chatbot by supporting multi-document workflows, document comparison, chat history management, source tracking, streaming responses, and an interactive document viewer.

## Features

### Document Management

* Upload and process multiple PDF documents
* View all uploaded documents
* Delete documents when no longer needed
* Automatic text extraction from PDFs
* Chunking and indexing of document content

### Intelligent Question Answering

* Ask questions across one or multiple PDFs
* Retrieval-Augmented Generation (RAG) pipeline
* Context-aware answers powered by Google Gemini
* Semantic search using vector embeddings
* Source citations for transparency and verification

### Multi-Document Comparison

* Compare information across multiple PDFs
* Identify similarities and differences between documents
* Generate consolidated responses from multiple sources

### Advanced Retrieval Pipeline

* Vector search using ChromaDB
* Semantic embeddings using Sentence Transformers
* Reranking of retrieved chunks for improved relevance
* Context filtering before response generation

### Chat Experience

* Real-time streaming responses
* Stop response generation while streaming
* Regenerate responses
* Persistent chat history
* Session-based conversations

### User Interface

* Modern React-based frontend
* Responsive design
* Integrated PDF viewer
* Source navigation
* Clean chat interface

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* Tailwind CSS
* Axios

### Backend

* FastAPI
* Python
* Uvicorn
* Pydantic

### AI & Retrieval

* Google Gemini
* ChromaDB
* Sentence Transformers
* Vector Embeddings
* Semantic Search
* Retrieval-Augmented Generation (RAG)

### Document Processing

* PyMuPDF (fitz)
* PDF Text Extraction
* Document Chunking

## Project Architecture

```text
User Query
    │
    ▼
FastAPI Backend
    │
    ▼
Semantic Retrieval
(ChromaDB + Embeddings)
    │
    ▼
Reranking Layer
    │
    ▼
Relevant Context Chunks
    │
    ▼
Google Gemini
    │
    ▼
Answer + Source Citations
    │
    ▼
React Frontend
```

## Current Functionality

✅ Upload multiple PDF documents

✅ Semantic search across uploaded documents

✅ AI-powered question answering

✅ Multi-document comparison

✅ Source citations

✅ Streaming responses

✅ Stop generation

✅ Regenerate responses

✅ Chat history management

✅ Document management

✅ PDF viewing support

✅ Reranking for improved retrieval quality

## Project Structure

```text
rag-chatbot/
│
├── rag-backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── chroma_db/
│   └── requirements.txt
│
├── rag-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   │
│   ├── public/
│   └── package.json
│
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/NehalSahu2004/rag-chatbot.git
cd rag-chatbot
```

## Backend Setup

Navigate to the backend directory:

```bash
cd rag-backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Start the backend server:

```bash
uvicorn app.main:app --reload --port 9000
```

Backend will run at:

```text
http://localhost:9000
```

## Frontend Setup

Navigate to the frontend directory:

```bash
cd rag-frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

## API Overview

### Document APIs

* Upload PDF documents
* List uploaded documents
* Delete documents

### Chat APIs

* Ask questions
* Compare documents
* Stream responses
* Regenerate responses

### History APIs

* Retrieve chat history
* Manage conversation sessions

## Future Enhancements

### Authentication & User Management

* JWT Authentication
* User Registration and Login
* User-specific PDF Storage
* User-specific Chat History
* Role-Based Access Control

### Infrastructure

* Docker Support
* Cloud Deployment
* CI/CD Pipeline
* Database Integration

### AI Improvements

* Hybrid Search
* Advanced Reranking Models
* Multi-modal Document Support
* Improved Citation Accuracy

## Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-Augmented Generation (RAG)
* Large Language Model Integration
* FastAPI Backend Development
* React Frontend Development
* Vector Databases
* Semantic Search
* Document Processing Pipelines
* API Design
* Full-Stack Application Development

## Author

Nehal Sahu

GitHub: https://github.com/NehalSahu2004

---

If you found this project useful, consider giving the repository a ⭐ on GitHub.

## Author

Nehal Sahu
