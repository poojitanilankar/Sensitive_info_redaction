
import re
import uuid
import fitz

from docx import Document


def redact_text(text, detections, method="blackout"):
    """
    Redact detected sensitive information.

    Returns:
        redacted_text, token_map
    """

    token_map = {}

    # Process from right to left to preserve positions.
    detections = sorted(
        detections,
        key=lambda x: x["start"],
        reverse=True
    )

    for item in detections:
        value = item["value"]

        if method == "blackout":
            replacement = "[REDACTED]"

        elif method == "partial":
            if len(value) <= 4:
                replacement = "*" * len(value)
            else:
                replacement = (
                    "*" * (len(value) - 4) + value[-4:]
                )

        elif method == "token":
            token = f"TOKEN_{uuid.uuid4().hex[:8].upper()}"
            replacement = token
            token_map[token] = value

        else:
            raise ValueError("Invalid redaction method")

        text = (
            text[:item["start"]]
            + replacement
            + text[item["end"]:]
        )

    return text, token_map


def redact_pdf(file_bytes, detections, method="blackout"):
    """
    Applies actual PDF redaction annotations
    for detected values found in selectable PDF text.
    """

    pdf = fitz.open(stream=file_bytes, filetype="pdf")

    token_map = {}

    for item in detections:

        value = item["value"]

        if method == "blackout":
            replacement = "[REDACTED]"

        elif method == "partial":
            replacement = (
                "*" * max(0, len(value) - 4) + value[-4:]
            )

        elif method == "token":
            replacement = (
                f"TOKEN_{uuid.uuid4().hex[:8].upper()}"
            )
            token_map[replacement] = value

        else:
            raise ValueError("Invalid redaction method")

        for page in pdf:

            rectangles = page.search_for(value)

            for rect in rectangles:
                page.add_redact_annot(
                    rect,
                    text=replacement,
                    fill=(0, 0, 0) if method == "blackout"
                    else (1, 1, 1),
                    text_color=(1, 1, 1) if method == "blackout"
                    else (0, 0, 0)
                )

    for page in pdf:
        page.apply_redactions()

    output = pdf.tobytes(garbage=4, deflate=True)
    pdf.close()

    return output, token_map


def redact_docx(file_bytes, detections, method="blackout"):
    """
    Redacts sensitive information in DOCX paragraphs.
    """

    import io

    document = Document(io.BytesIO(file_bytes))

    token_map = {}

    def replace_in_paragraph(paragraph):
        original = paragraph.text

        updated, tokens = redact_text(
            original,
            detections_for_text(original, detections),
            method
        )

        token_map.update(tokens)

        if updated != original:
            paragraph.clear()
            paragraph.add_run(updated)

    for paragraph in document.paragraphs:
        replace_in_paragraph(paragraph)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_in_paragraph(paragraph)

    output = io.BytesIO()
    document.save(output)

    return output.getvalue(), token_map


def detections_for_text(text, detections):
    """
    Recalculate positions for each individual paragraph.
    """

    results = []

    for item in detections:
        value = item["value"]

        for match in re.finditer(re.escape(value), text):
            results.append({
                **item,
                "start": match.start(),
                "end": match.end()
            })

    return results
