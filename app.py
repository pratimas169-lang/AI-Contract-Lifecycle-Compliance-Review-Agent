import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Contract Review Agent",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("AI Contract Lifecycle & Compliance Review Agent")

st.write(
    "Review contract clauses against approved company policies "
    "and generate an evidence-grounded review for human approval."
)

st.divider()

# Contract upload
st.subheader("1. Upload Contract")

uploaded_file = st.file_uploader(
    "Upload a contract document",
    type=["docx", "pdf"]
)

# Review question
st.subheader("2. Review Task")

review_question = st.text_input(
    "Enter your review question",
    value="Does this contract comply with the standard payment policy?"
)

# Review button
st.subheader("3. Start Review")

if st.button("Run Contract Review"):
    if uploaded_file is None:
        st.warning("Please upload a contract document first.")
    else:
        st.success("Contract uploaded successfully.")
        st.info("Starting AI contract review workflow...")

        import requests

        webhook_url = "http://localhost:5678/webhook/contract-review"

        payload = {
            "review_question": review_question
        }

        response = requests.post(
            webhook_url,
            json=payload
        )

        if response.status_code == 200:
            st.success("Contract review workflow started successfully.")
        else:
            st.error(
                f"Unable to start the workflow. "
                f"Status code: {response.status_code}"
            )