# pip install streamlit langchain-google-genai PyPDF2 pandas

import os, re, json, io
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI

# ──────────────────────────────────────────────────────────
# 🔑  Sidebar – API key & job description
# ──────────────────────────────────────────────────────────
st.set_page_config(page_title="Gemini Resume Matcher", page_icon="📄", layout="wide")
st.title("📄 Gemini-powered Resume Matcher")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Google Gemini API key", type="password")
    job_desc = st.text_area("Job Description", height=250,
                            placeholder="Paste the JD here …")
    temperature = st.slider("Model Temperature", 0.0, 1.0, 0.3)
    max_tokens  = st.slider("Max Tokens", 256, 4096, 1024, step=256)

if not api_key:
    st.info("Add your Gemini API key in the sidebar to begin.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=temperature,
    max_tokens=max_tokens,
    google_api_key=api_key,
)

# ──────────────────────────────────────────────────────────
# 📥  Helpers
# ──────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def extract_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def analyze_resume(content: str, filename: str) -> dict:
    prompt = f"""
You are an expert technical recruiter.

JOB DESCRIPTION:
{job_desc}

RESUME ({filename}):
{content}

Return ONLY valid JSON like:
{{
  "filename":"{filename}",
  "match_percentage":25,
  "overall_fit":"MODERATE",
  "key_strengths":["..."],
  "matching_skills":["..."],
  "missing_requirements":["..."],
  "experience_level":"JUNIOR",
  "summary":"brief text",
  "recommendation":"CONSIDER"
}}
"""
    try:
        res_txt = llm.invoke(prompt).content
        data = json.loads(re.search(r"{.*}", res_txt, re.S).group())
    except Exception:
        data = {
            "filename": filename,
            "match_percentage": 0,
            "overall_fit": "ERROR",
            "key_strengths": [],
            "matching_skills": [],
            "missing_requirements": [],
            "experience_level": "UNKNOWN",
            "summary": "Failed to parse model response.",
            "recommendation": "ERROR",
        }
    return data

# ──────────────────────────────────────────────────────────
# 📑  Upload & analyse resumes
# ──────────────────────────────────────────────────────────
uploaded_files = st.file_uploader("Upload PDF resumes", type="pdf",
                                  accept_multiple_files=True)

if uploaded_files and job_desc and st.button("🚀 Analyse Resumes"):
    results = []
    for file in uploaded_files:
        with st.spinner(f"Analysing {file.name} …"):
            text = extract_text(file.getvalue())
            results.append(analyze_resume(text, file.name))

    # sort by score & show table
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    df = pd.DataFrame(results)
    st.subheader("🏆 Ranking")
    st.dataframe(df[["filename","match_percentage","overall_fit",
                     "experience_level","recommendation"]], use_container_width=True)

    # expandable details
    for r in results:
        with st.expander(f"{r['filename']}  —  {r['match_percentage']}%  ({r['overall_fit']})"):
            st.markdown(f"**Summary:** {r['summary']}")
            st.markdown(f"**Key strengths:** {', '.join(r['key_strengths'])}")
            st.markdown(f"**Matching skills:** {', '.join(r['matching_skills'])}")
            if r["missing_requirements"]:
                st.markdown(f"**Missing requirements:** {', '.join(r['missing_requirements'])}")
            st.markdown(f"**Recommendation:** {r['recommendation']}")
else:
    st.markdown("### ↑ Upload PDFs and press **Analyse Resumes** to start.")