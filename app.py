import streamlit as st
from llm_client import review_resume_with_openai
import PyPDF2

st.set_page_config(page_title="Resume Reviewer", layout="wide")
st.title("📝 AI Resume Reviewer")

# Sidebar: Resume input
st.sidebar.header("Resume Input")
uploaded_file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])
paste_text = st.sidebar.text_area("Or paste your resume text here", height=200)

# Sidebar: Target role
target_role = st.sidebar.text_input("Target Job Role (e.g., Data Scientist)")
job_desc = st.sidebar.text_area("Optional: Paste Job Description here", height=150)

# Sidebar: Model selection
model_choice = st.sidebar.selectbox(
    "Select LLM Model",
    ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"]
)

# Extract text from uploaded PDF if provided
resume_text = ""
if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        resume_text += page.extract_text() + "\n"
elif paste_text.strip() != "":
    resume_text = paste_text
else:
    st.warning("Please upload a PDF or paste your resume text.")
    st.stop()

# Run LLM review when button clicked
if st.sidebar.button("Review Resume"):
    with st.spinner("Analyzing resume..."):
        result = review_resume_with_openai(resume_text, target_role, job_desc, model=model_choice)
    
    # Option B: result is a dictionary
    if isinstance(result, dict):
        st.metric("Overall Score", result.get("overall_score", "N/A"))
        st.subheader("Highlights")
        st.write(result.get("highlights", "No highlights available."))
        st.subheader("Weaknesses / Suggestions")
        st.write(result.get("weaknesses", "No weaknesses detected."))
        st.subheader("Full Feedback")
        st.code(result.get("feedback", "No feedback available."))
    else:
        # fallback if result is just a string
        st.code(result)
