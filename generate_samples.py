
from pathlib import Path

import fitz
from docx import Document


SAMPLE_TEXT = """
SENSITIVE INFORMATION SHIELD - SAMPLE DOCUMENT

Name: Rahul Sharma

Aadhaar: 2345 6789 0123
PAN: ABCDE1234F
Phone: 9876543210
Email: rahul@example.com

Bank Account: 123456789012
IFSC: SBIN0001234
UPI: rahul@oksbi

Card Number: 4532015112830366

This document contains fictional test data.
Do not use these values for real transactions.
"""


def generate_samples():
    folder = Path("samples")
    folder.mkdir(exist_ok=True)

    # Generate TXT
    (folder / "sample.txt").write_text(
        SAMPLE_TEXT,
        encoding="utf-8"
    )

    # Generate DOCX
    document = Document()
    document.add_heading(
        "Sensitive Information Shield - Sample",
        level=1
    )

    for line in SAMPLE_TEXT.splitlines():
        document.add_paragraph(line)

    document.save(folder / "sample.docx")

    # Generate PDF
    pdf = fitz.open()
    page = pdf.new_page()

    page.insert_textbox(
        fitz.Rect(50, 50, 550, 750),
        SAMPLE_TEXT,
        fontsize=11
    )

    pdf.save(folder / "sample.pdf")
    pdf.close()

    print("Sample files generated successfully!")


if __name__ == "__main__":
    generate_samples()
