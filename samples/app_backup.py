
import streamlit as st
import pandas as pd

from pathlib import Path

from detectors import detect_sensitive_data
from extractors import extract_text
from redactor import (
    redact_text,
    redact_pdf,
    redact_docx
)


st.set_page_config(
    page_title="Sensitive Information Shield",
    page_icon="🛡️",
    layout="wide"
)


st.title("🛡️ Sensitive Information Shield")

st.markdown(
    "### Detect, analyse and protect sensitive information "
    "in your documents."
)

st.info(
    "Your uploaded files are processed locally in this "
    "application. Avoid uploading real personal or financial "
    "information during testing."
)


uploaded_file = st.file_uploader(
    "Upload your document",
    type=["txt", "pdf", "docx", "png", "jpg", "jpeg"]
)


if uploaded_file:

    file_bytes = uploaded_file.getvalue()
    filename = uploaded_file.name
    extension = Path(filename).suffix.lower()

    try:
        extracted = extract_text(file_bytes, filename)
        text = extracted["text"]

        if extracted.get("warning"):
            st.warning(extracted["warning"])

        if not text.strip():
            st.error("No text could be extracted.")
            st.stop()

        st.subheader("1. Extracted Content")

        st.text_area(
            "Document text",
            text,
            height=220
        )

        st.subheader("2. Sensitive Information Detection")

        detections = detect_sensitive_data(text)

        if detections:

            st.success(
                f"{len(detections)} potential sensitive "
                "items detected."
            )

            report = pd.DataFrame([
                {
                    "Type": item["type"],
                    "Detected Value": item["value"],
                    "Confidence": item["confidence"],
                    "Start": item["start"],
                    "End": item["end"]
                }
                for item in detections
            ])

            st.dataframe(
                report,
                use_container_width=True
            )

        else:
            st.warning("No sensitive information detected.")

        st.subheader("3. Redaction")

        method = st.selectbox(
            "Choose redaction method",
            ["blackout", "partial", "token"]
        )

        if st.button("Redact Document", type="primary"):

            if not detections:
                st.warning("Nothing to redact.")
                st.stop()

            if extension == ".pdf":
                output, token_map = redact_pdf(
                    file_bytes,
                    detections,
                    method
                )
                output_name = "redacted_" + filename

            elif extension == ".docx":
                output, token_map = redact_docx(
                    file_bytes,
                    detections,
                    method
                )
                output_name = "redacted_" + filename

            elif extension == ".txt":
                output, token_map = redact_text(
                    text,
                    detections,
                    method
                )
                output = output.encode("utf-8")
                output_name = "redacted_" + filename

            else:
                st.error(
                    "Image redaction is not implemented yet. "
                    "OCR currently extracts text only."
                )
                st.stop()

            st.session_state["redacted_output"] = output
            st.session_state["output_name"] = output_name
            st.session_state["token_map"] = token_map

            st.success("Redaction completed!")

        if "redacted_output" in st.session_state:

            st.subheader("4. Download Protected Document")

            st.download_button(
                label="Download Redacted File",
                data=st.session_state["redacted_output"],
                file_name=st.session_state["output_name"],
                mime="application/octet-stream"
            )

            token_map = st.session_state["token_map"]

            if token_map:
                st.warning(
                    "Token mapping contains original sensitive "
                    "values. Store it securely and separately."
                )

                st.json(token_map)

    except Exception as error:
        st.error(f"Processing error: {error}")


st.divider()

st.caption(
    "Sensitive Information Shield | CB-02 | "
    "Local document protection prototype"
)
