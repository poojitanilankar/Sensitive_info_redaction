
import io
from pathlib import Path

import fitz
from docx import Document
from PIL import Image
import pytesseract


def extract_text(file_bytes, filename):
    """
    Extract text from uploaded files.

    Returns:
        {
            "text": extracted text,
            "filename": filename,
            "file_type": extension,
            "warning": optional warning
        }
    """

    extension = Path(filename).suffix.lower()

    try:
        if extension == ".txt":
            text = file_bytes.decode("utf-8", errors="replace")

        elif extension == ".pdf":
            pdf = fitz.open(stream=file_bytes, filetype="pdf")
            text = "\n".join(
                page.get_text() for page in pdf
            )
            pdf.close()

            warning = (
                "PDF text extraction may not detect scanned content."
                if not text.strip() else None
            )

            return {
                "text": text,
                "filename": filename,
                "file_type": extension,
                "warning": warning
            }

        elif extension == ".docx":
            document = Document(io.BytesIO(file_bytes))

            paragraphs = [
                p.text for p in document.paragraphs
            ]

            for table in document.tables:
                for row in table.rows:
                    paragraphs.append(
                        " | ".join(cell.text for cell in row.cells)
                    )

            text = "\n".join(paragraphs)

        elif extension in [".png", ".jpg", ".jpeg"]:
            image = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(image)

        else:
            raise ValueError("Unsupported file format")

        return {
            "text": text,
            "filename": filename,
            "file_type": extension,
            "warning": None
        }

    except Exception as error:
        raise RuntimeError(
            f"Could not extract text: {error}"
        ) from error
