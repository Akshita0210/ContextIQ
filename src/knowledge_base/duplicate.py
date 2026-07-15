import hashlib


def compute_file_hash(pdf_path: str) -> str:
    """
    Compute the SHA-256 hash of a PDF file.

    Args:
        pdf_path (str): Path to the PDF.

    Returns:
        str: SHA-256 hash as a hexadecimal string.
    """

    sha256 = hashlib.sha256()

    with open(pdf_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def compute_uploaded_file_hash(uploaded_file) -> str:
    """
    Compute SHA-256 hash directly from a Streamlit UploadedFile.
    """

    sha256 = hashlib.sha256()

    sha256.update(uploaded_file.getvalue())

    return sha256.hexdigest()