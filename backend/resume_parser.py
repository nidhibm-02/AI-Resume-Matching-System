
import fitz
from docx import Document
from io import BytesIO


def extract_text_from_pdf(file_bytes):
    """Extract text from a PDF resume."""
    text = ""

    pdf = fitz.open(stream=file_bytes, filetype="pdf")

    for page in pdf:
        text += page.get_text() + "\n"

    pdf.close()
    return text.strip()


def extract_text_from_docx(file_bytes):
    """Extract text from a DOCX resume."""
    document = Document(BytesIO(file_bytes))

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

    return text.strip()


def extract_resume_text(filename, file_bytes):
    """Identify the file type and extract resume text."""

    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    else:
        raise ValueError("Only PDF and DOCX files are supported.")
