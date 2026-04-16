import streamlit as st
from dotenv import load_dotenv
from utils.pdf_parser import extract_text_from_pdf, chunk_text
from utils.embeddings import build_vector_store
from utils.qa_chain import answer_question

load_dotenv()

MAX_QUESTIONS_PER_SESSION = 20

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Document AI — StarForge",
    page_icon="📄",
    layout="centered"
)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("📄 Document AI")
st.caption("Upload any PDF and ask it questions in plain English.")
st.divider()

# ── Session state init ────────────────────────────────────────────────────────
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

# ── File Upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf",
    help="Supported: any text-based PDF. Scanned image PDFs may not work well."
)

if uploaded_file is not None:
    # Only re-process if a NEW file is uploaded
    if st.session_state.pdf_name != uploaded_file.name:
        with st.spinner(f"Processing '{uploaded_file.name}'..."):
            # Step 1: Extract text
            try:
                raw_text = extract_text_from_pdf(uploaded_file)
            except ValueError as exc:
                st.error(str(exc))
                st.stop()
            except Exception:
                st.error("Unable to process this PDF. Please try a different file.")
                st.stop()
            
            # Step 2: Chunk it
            chunks = chunk_text(raw_text)
            if not chunks:
                st.error("No readable text found in this PDF.")
                st.stop()
            
            # Step 3: Build vector store
            try:
                st.session_state.vector_store = build_vector_store(chunks)
            except Exception:
                st.error("Failed to build search index for this PDF.")
                st.stop()
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.messages = []  # Reset chat on new upload
            st.session_state.question_count = 0
        
        st.success(f"✅ '{uploaded_file.name}' processed — {len(chunks)} chunks indexed.")

# ── Chat Interface ────────────────────────────────────────────────────────────
if st.session_state.vector_store is not None:
    st.subheader(f"💬 Ask about: {st.session_state.pdf_name}")
    
    # Display existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander("📎 Source passages"):
                    for i, source in enumerate(msg["sources"], 1):
                        st.caption(f"Source {i}: {source}")
    
    # Chat input
    if question := st.chat_input("Ask a question about your document..."):
        if st.session_state.question_count >= MAX_QUESTIONS_PER_SESSION:
            st.error("Session limit reached. Please refresh the page to continue.")
            st.stop()
        if not question.strip():
            st.error("Please enter a question.")
            st.stop()
        # Show user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        
        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = answer_question(st.session_state.vector_store, question)
                except ValueError as exc:
                    st.error(str(exc))
                    st.stop()
                except Exception:
                    st.error("Unable to answer this question right now. Please try again.")
                    st.stop()
            st.write(result["answer"])
            with st.expander("📎 Source passages"):
                for i, source in enumerate(result["sources"], 1):
                    st.caption(f"Source {i}: {source}")
        
        # Save assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"]
        })
        st.session_state.question_count += 1

else:
    # Placeholder UI when no PDF is uploaded
    st.info("👆 Upload a PDF above to get started. Works with contracts, reports, manuals, and more.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Supported formats", "PDF")
    with col2:
        st.metric("Powered by", "GPT-4o-mini")
    with col3:
        st.metric("Built By", "StarForge")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Built by [StarForge](https://your-site.com) · Powered by OpenAI + LangChain")
