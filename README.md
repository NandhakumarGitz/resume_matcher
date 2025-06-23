# 📄 Gemini-powered Resume Matcher

This project is a **Streamlit-based web application** that uses **Google Gemini (Gemini 1.5 Flash)** to automatically evaluate and rank resumes (PDF files) against a given **job description**. It helps HR or technical recruiters to make better shortlisting decisions using AI.

---

## ✅ What I Did in This Project

✔️ Integrated **Google Gemini API** using `langchain-google-genai`  
✔️ Built an interactive UI using **Streamlit**  
✔️ Developed a **custom prompt template** to extract structured JSON from the LLM  
✔️ Implemented **PDF text extraction** using `PyPDF2`  
✔️ Used **regular expressions** and **error handling** to manage LLM responses  
✔️ Displayed AI evaluation results using **interactive tables and expandable sections**  
✔️ Allowed multiple resume uploads and **ranking based on match percentage**  
✔️ Configured **temperature** and **max token** sliders for LLM customization  

---

## 🚀 Features

- 🔐 Secure API key input via sidebar
- 📄 Upload and analyze multiple PDF resumes
- 💼 Paste job description directly into the interface
- 🤖 Uses Gemini 1.5 Flash to generate structured resume evaluation
- 📊 Displays results with percentage match and recommendations
- 🔄 Adjustable LLM settings: temperature and max tokens
- 🧾 Full support for batch processing and data export

---

## 📦 Technologies Used

- **Python**
- **Streamlit**
- **LangChain (Google Generative AI integration)**
- **PyPDF2**
- **pandas**
- **Regular Expressions (re)**

--
