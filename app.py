
import streamlit as st
import pandas as pd
import hashlib

from pathlib import Path

from detectors import detect_sensitive_data
from extractors import extract_text
from redactor import (
    redact_text,
    redact_pdf,
    redact_docx
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SENTINEL | Sensitive Information Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>


html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0B1421;
    color: #E8EEF5;
}

[data-testid="stSidebar"] {
    background: #101E2D;
    border-right: 1px solid #26394B;
}

[data-testid="stSidebar"] * {
    color: #DCE7F1;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1, h2, h3 {
    color: #F1F5F9 !important;
}

p, label {
    color: #B8C7D8;
}

.hero {
    background: linear-gradient(120deg, #142C40, #123B42);
    border: 1px solid #285263;
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 8px;
    color: #FFFFFF !important;
}

.hero p {
    color: #B8CEDB;
    font-size: 15px;
}

.metric-card {
    background: #142437;
    border: 1px solid #263D53;
    padding: 22px;
    border-radius: 15px;
    min-height: 125px;
}

.metric-label {
    color: #A8B9CB;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 800;
    margin-top: 10px;
}

.section-title {
    color: #F1F5F9;
    font-size: 20px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

.info-card {
    background: #142437;
    border: 1px solid #263D53;
    border-radius: 15px;
    padding: 22px;
}

.security-note {
    background: #10352F;
    border: 1px solid #236A56;
    border-radius: 12px;
    padding: 15px;
    color: #A7F3D0;
    margin: 15px 0;
}

.upload-note {
    background: #142437;
    border: 1px dashed #3B6577;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
}

.stButton > button {
    background: #0D9488;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    padding: 10px 22px;
}

.stButton > button:hover {
    background: #0F766E;
    color: white;
    border: none;
}

.stDownloadButton > button {
    background: #0D9488;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

[data-testid="stFileUploader"] {
    background: #142437;
    border: 1px dashed #3B6577;
    border-radius: 13px;
    padding: 12px;
}

hr {
    border-color: #26394B;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

for key, default in {
    "redacted_output": None,
    "output_name": None,
    "token_map": None,
    "file_key": None,
    "text": "",
    "detections": [],
    "filename": "",
    "file_bytes": None,
    "extension": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def mask_value(value):
    """Hide sensitive values in the findings table."""
    value = str(value)

    if len(value) <= 4:
        return "X" * len(value)

    return "X" * (len(value) - 4) + value[-4:]


def metric_card(label, value, icon):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="padding:15px 5px 25px 5px;">
        <div style="font-size:30px;">🛡️</div>
        <div style="font-size:23px;font-weight:800;color:#5EEAD4;">
            SENTINEL
        </div>
        <div style="font-size:10px;letter-spacing:2px;color:#9CB2C6;">
            INFORMATION SHIELD
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### NAVIGATION")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Document Scanner",
            "Detection Results",
            "Redaction Center",
            "About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### SECURITY STATUS")

    st.markdown("""
    <div class="security-note">
        🟢 <b>LOCAL PROCESSING</b><br>
        <small>Your documents are processed locally by this application.</small>
    </div>
    """, unsafe_allow_html=True)

    st.caption("CB-02 | Hackathon Prototype")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>🛡️ SENTINEL</h1>
    <p>
        Intelligent Sensitive Information Detection
        & Document Protection
    </p>
    <div style="color:#5EEAD4;font-size:12px;font-weight:700;">
        PRIVACY FIRST • SECURE PROCESSING • DOCUMENT PROTECTION
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.markdown(
        '<div class="section-title">Security Overview</div>',
        unsafe_allow_html=True
    )

    total = len(st.session_state.detections)
    protected = (
        1 if st.session_state.redacted_output is not None else 0
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card("CURRENT FINDINGS", total, "🔎")

    with c2:
        metric_card("PROTECTED DOCUMENTS", protected, "🛡️")

    with c3:
        metric_card(
            "PROCESSING MODE",
            "LOCAL",
            "🔒"
        )

    st.markdown(
        '<div class="section-title">Welcome to your security workspace</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <h3>Protect your sensitive documents</h3>
        <p>
            Scan documents to identify sensitive information,
            review detected values and choose how to protect them.
        </p>
        <p>
            <b style="color:#5EEAD4;">Supported formats:</b>
            PDF · DOCX · TXT · PNG · JPG
        </p>
        <p>
            <b style="color:#5EEAD4;">Detection:</b>
            Aadhaar · PAN · Phone · Email · Card · UPI · IFSC · Bank Account
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">How SENTINEL works</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="info-card">
            <h3>01 · Upload</h3>
            <p>Upload your document for local processing.</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="info-card">
            <h3>02 · Detect</h3>
            <p>Identify and review sensitive information.</p>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="info-card">
            <h3>03 · Protect</h3>
            <p>Redact sensitive information and download the result.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("Use Document Scanner in the sidebar to begin.")


# --------------------------------------------------
# DOCUMENT SCANNER
# --------------------------------------------------

elif page == "Document Scanner":

    st.markdown(
        '<div class="section-title">Document Scanner</div>',
        unsafe_allow_html=True
    )

    st.write("Upload a document to extract and analyse its content.")

    uploaded_file = st.file_uploader(
        "Choose your document",
        type=["txt", "pdf", "docx", "png", "jpg", "jpeg"],
        key="document_upload"
    )

    if uploaded_file:

        file_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name
        extension = Path(filename).suffix.lower()

        file_key = hashlib.sha256(file_bytes).hexdigest()

        if st.session_state.file_key != file_key:

            st.session_state.redacted_output = None
            st.session_state.output_name = None
            st.session_state.token_map = None

            with st.spinner("Extracting and analysing document..."):

                try:

                    extracted = extract_text(file_bytes, filename)
                    text = extracted["text"]

                    if extracted.get("warning"):
                        st.warning(extracted["warning"])

                    if not text.strip():
                        st.error("No text could be extracted.")
                        st.stop()

                    detections = detect_sensitive_data(text)

                    st.session_state.file_key = file_key
                    st.session_state.text = text
                    st.session_state.detections = detections
                    st.session_state.filename = filename
                    st.session_state.file_bytes = file_bytes
                    st.session_state.extension = extension

                except Exception as error:
                    st.error(f"Processing error: {error}")
                    st.stop()

        st.success(f"Document loaded: {filename}")

        st.markdown("### Extracted Document Content")

        with st.expander("View extracted text", expanded=False):
            st.text_area(
                "Extracted content",
                st.session_state.text,
                height=250,
                disabled=True
            )

        detections = st.session_state.detections

        high_risk_types = {
            "AADHAAR", "PAN", "CARD", "BANK_ACCOUNT"
        }

        high_count = sum(
            item["type"].upper() in high_risk_types
            for item in detections
        )

        m1, m2, m3 = st.columns(3)

        with m1:
            metric_card("TOTAL FINDINGS", len(detections), "🔍")

        with m2:
            metric_card("HIGH-RISK FINDINGS", high_count, "🔴")

        with m3:
            metric_card(
                "OTHER FINDINGS",
                len(detections) - high_count,
                "🟠"
            )

        if detections:
            st.success(
                f"{len(detections)} potential sensitive items detected."
            )
        else:
            st.warning("No sensitive information detected.")


# --------------------------------------------------
# DETECTION RESULTS
# --------------------------------------------------

elif page == "Detection Results":

    st.markdown(
        '<div class="section-title">Detection Results</div>',
        unsafe_allow_html=True
    )

    detections = st.session_state.detections

    if not st.session_state.file_key:
        st.info("Upload a document in Document Scanner first.")

    elif not detections:
        st.success("No sensitive information was detected.")

    else:

        st.write(
            "Review detected information. Values are masked for privacy."
        )

        report = pd.DataFrame([
            {
                "Type": item["type"],
                "Detected Value": mask_value(item["value"]),
                "Confidence": item["confidence"],
                "Start": item["start"],
                "End": item["end"]
            }
            for item in detections
        ])

        st.dataframe(
            report,
            width="stretch",
            hide_index=True
        )

        st.markdown("### Findings by category")

        counts = report["Type"].value_counts()

        st.bar_chart(counts)


# --------------------------------------------------
# REDACTION CENTER
# --------------------------------------------------

elif page == "Redaction Center":

    st.markdown(
        '<div class="section-title">Redaction Center</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.file_key:
        st.info("Upload a document in Document Scanner first.")

    else:

        st.write("Choose how sensitive information should be protected.")

        method = st.selectbox(
            "Redaction method",
            ["blackout", "partial", "token"]
        )

        method_info = {
            "blackout": "Completely hides sensitive values.",
            "partial": "Masks most characters while retaining the last four.",
            "token": "Replaces values with generated identifiers."
        }

        st.info(method_info[method])

        detections = st.session_state.detections
        extension = st.session_state.extension
        filename = st.session_state.filename
        file_bytes = st.session_state.file_bytes

        if st.button(
            "🛡️ Apply Redaction",
            type="primary",
            width="stretch",
            disabled=not detections
        ):

            try:

                with st.spinner("Protecting your document..."):

                    if extension == ".pdf":

                        output, token_map = redact_pdf(
                            file_bytes,
                            detections,
                            method
                        )

                    elif extension == ".docx":

                        output, token_map = redact_docx(
                            file_bytes,
                            detections,
                            method
                        )

                    elif extension == ".txt":

                        output, token_map = redact_text(
                            st.session_state.text,
                            detections,
                            method
                        )

                        output = output.encode("utf-8")

                    else:
                        st.error(
                            "Image redaction is not implemented "
                            "in the current backend."
                        )
                        st.stop()

                    st.session_state.redacted_output = output
                    st.session_state.output_name = (
                        "redacted_" + filename
                    )
                    st.session_state.token_map = token_map

                st.success("Redaction completed successfully!")

            except Exception as error:
                st.error(f"Redaction error: {error}")

        if st.session_state.redacted_output is not None:

            st.markdown("### Protected Document")

            st.success("Your redacted file is ready.")

            st.download_button(
                "⬇️ Download Protected Document",
                data=st.session_state.redacted_output,
                file_name=st.session_state.output_name,
                mime="application/octet-stream",
                width="stretch"
            )

            token_map = st.session_state.token_map

            if token_map:
                st.warning(
                    "The token mapping contains original sensitive "
                    "values. Do not share it publicly."
                )

                with st.expander("View token mapping"):
                    st.json(token_map)


# --------------------------------------------------
# ABOUT
# --------------------------------------------------

elif page == "About":

    st.markdown(
        '<div class="section-title">About SENTINEL</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <h2>🛡️ Sensitive Information Shield</h2>

        <p>
            SENTINEL is a document privacy prototype designed
            to detect and protect sensitive information in documents.
        </p>

        <h3>Core capabilities</h3>

        <ul>
            <li>Indian sensitive information detection</li>
            <li>Document text extraction</li>
            <li>Multiple redaction methods</li>
            <li>Local document processing</li>
            <li>Protected document downloads</li>
        </ul>

        <h3>Technology stack</h3>

        <p>Python · Streamlit · Pandas · PyMuPDF · OCR · Regex</p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<div style="text-align:center;color:#8296AA;font-size:12px;padding:15px;">
    🛡️ SENTINEL | CB-02<br>
    Sensitive Information Shield<br>
    Privacy First · Local Processing
</div>
""", unsafe_allow_html=True)
