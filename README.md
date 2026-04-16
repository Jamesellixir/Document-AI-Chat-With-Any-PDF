# Document AI - Chat With Any PDF

> StarForge portfolio project | AI-powered PDF question answering demo

Live Demo: [replace with your deployed Streamlit URL](https://document-ai-chat-with-any-pdf.streamlit.app/)

## Overview

Document AI is a clean, client-ready document intelligence demo that lets users upload a PDF and ask natural language questions about its content. It extracts text, chunks it for retrieval, builds an in-memory FAISS index, and returns sourced answers using OpenAI + LangChain.

Built for the StarForge portfolio, this project is designed to show practical delivery, clear UI, and production-minded engineering without unnecessary scope creep.

## What It Does

- Upload a PDF through a simple Streamlit interface
- Extract text from each page with PyMuPDF
- Split the document into retrieval-friendly chunks
- Create an in-memory FAISS vector index
- Answer questions with GPT-4o-mini using document context only
- Show relevant source passages alongside each answer

## Why It Matters

- Demonstrates a real RAG workflow end to end
- Proves ability to build and ship a usable AI demo quickly
- Fits a strong portfolio niche for document intelligence, AI support tools, and knowledge assistants
- Shows a professional stack: Python, Streamlit, LangChain, OpenAI, FAISS

## Key Features

- Single PDF upload flow
- Context-based Q&A with source passages
- Session memory for chat continuity
- Input and file safeguards
- Clean fallback states when no PDF is loaded
- Lightweight, public-demo friendly architecture

## Tech Stack

| Layer | Tool |
| --- | --- |
| UI | Streamlit |
| PDF parsing | PyMuPDF |
| Text splitting | langchain-text-splitters |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector search | FAISS |
| LLM | GPT-4o-mini |
| Orchestration | LangChain |
| Env management | python-dotenv |

## Architecture

```text
PDF Upload -> Text Extraction -> Chunking -> Embeddings -> FAISS Retrieval -> GPT-4o-mini Answer
```

## Project Structure

```text
Document AI - Chat With Any PDF/
├── app.py
├── requirements.txt
├── README.md
├── SECURITY_AUDIT.md
├── .env.example
├── .gitignore
├── screenshots/
└── utils/
    ├── pdf_parser.py
    ├── embeddings.py
    └── qa_chain.py
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/document-ai.git
cd document-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

## How to Use

1. Upload a PDF.
2. Wait for processing to finish.
3. Ask a question in the chat box.
4. Review the answer and expand the source passages.

## Demo Questions

- What is the main topic of this document?
- Summarize section 2.
- What payment terms are mentioned in this contract?

## Reliability and Safety

- Maximum PDF size: 20MB
- Session question limit: 20 questions
- Questions are capped to reduce abuse and cost spikes
- Errors are handled gracefully in the UI
- The system is designed to answer from document context only

## Screenshots

-----
<img width="966" height="776" alt="Screenshot 2026-04-17 002158" src="https://github.com/user-attachments/assets/dd3d5a0e-1484-46b6-858e-f9bacc631f91" />
-----
<img width="1002" height="739" alt="Screenshot 2026-04-17 001903" src="https://github.com/user-attachments/assets/8f37a183-4d41-46a8-af23-2d87331e2f05" />
-----
<img width="1016" height="804" alt="Screenshot 2026-04-17 001701" src="https://github.com/user-attachments/assets/417b93ff-acf0-4d4b-9e0c-4f5559f02a09" />
-----
<img width="901" height="763" alt="Screenshot 2026-04-17 001646" src="https://github.com/user-attachments/assets/45934143-fdbd-455d-b4af-bd3898b845b8" />
-----
<img width="954" height="770" alt="Screenshot 2026-04-17 001521" src="https://github.com/user-attachments/assets/52acd652-136d-427e-801a-f4fadb3167f7" />
-----

## StarForge Branding

Document AI is part of the StarForge portfolio foundation: practical AI systems, fast delivery, and clean execution.
