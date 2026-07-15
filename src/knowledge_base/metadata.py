import os
from datetime import datetime
from pypdf import PdfReader

def extract_metadata(pdf_path: str) -> dict:
    """
    Extract basic metadata from a PDF.

    Args:
        pdf_path (str): Absolute/relative path of the PDF.

    Returns:
        dict
    """

    reader = PdfReader(pdf_path)

    metadata = {
        "filename": os.path.basename(pdf_path),
        "file_path": pdf_path,
        "pages": len(reader.pages),
        "file_size": os.path.getsize(pdf_path),
        "uploaded_at": datetime.now().isoformat(timespec="seconds")
    }

    return metadata