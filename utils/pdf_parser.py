import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

MAX_PDF_SIZE_MB = 20
MAX_PDF_SIZE_BYTES = MAX_PDF_SIZE_MB * 1024 * 1024

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract raw text from an uploaded Streamlit file object."""
    # Read bytes from the uploaded file
    pdf_bytes = uploaded_file.read()
    if len(pdf_bytes) > MAX_PDF_SIZE_BYTES:
        raise ValueError(
            f"PDF exceeds {MAX_PDF_SIZE_MB}MB limit. Please upload a smaller file."
        )
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError("Unable to read PDF. Please upload a valid PDF file.") from exc

    try:
        full_text = ""
        for page_num, page in enumerate(doc):
            full_text += f"\n\n--- Page {page_num + 1} ---\n"
            full_text += page.get_text()
        return full_text
    finally:
        doc.close()


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_text(text)
