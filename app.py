import streamlit as st
from pypdf import PdfReader

CHECKS = {
    "python": "Python skill",
    "project": "Projects section",
    "education": "Education details",
    "github": "GitHub link",
    "internship": "Internship mention",
    "file handling": "File handling skill",
}


def analyze_resume(text):
    text = text.lower()
    found, missing, suggestions = [], [], []

    for key, name in CHECKS.items():
        if key in text:
            found.append(name)
        else:
            missing.append(name)
            suggestions.append(f"Add {name}")

    words = len(text.split())
    if words < 150:
        suggestions.append("Resume is too short")
    elif words > 400:
        suggestions.append("Resume is too long")

    percent = int((len(found) / len(CHECKS)) * 100)
    if percent >= 70:
        strength = "Strong"
    elif percent >= 40:
        strength = "Average"
    else:
        strength = "Weak"

    return found, missing, words, percent, strength, suggestions


def read_pdf(file):
    reader = PdfReader(file)
    return "\n".join((page.extract_text() or "") for page in reader.pages)


st.set_page_config(page_title="Screening me", page_icon="📄")
st.title("📄screening me")
st.write("Apna resume upload karo ya text paste karo, aur turant analysis dekho.")

tab1, tab2 = st.tabs(["Upload PDF", "Paste text"])
resume_text = ""

with tab1:
    uploaded = st.file_uploader("Resume PDF choose karo", type=["pdf"])
    if uploaded is not None:
        try:
            resume_text = read_pdf(uploaded)
        except Exception:
            st.error("PDF read nahi ho paayi. Koi doosri PDF try karo.")

with tab2:
    pasted = st.text_area("Resume text yahan paste karo", height=250)
    if pasted.strip():
        resume_text = pasted

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Pehle resume upload karo ya text paste karo.")
    else:
        found, missing, words, percent, strength, suggestions = analyze_resume(resume_text)

        st.subheader("Result")
        st.progress(percent / 100)
        col1, col2, col3 = st.columns(3)
        col1.metric("Score", f"{percent}%")
        col2.metric("Strength", strength)
        col3.metric("Word Count", words)

        st.subheader("Checks")
        for name in found:
            st.success(f"✔ {name} found")
        for name in missing:
            st.error(f"✘ {name} missing")

        st.subheader("Suggestions")
        if suggestions:
            for s in suggestions:
                st.write("-", s)
        else:
            st.write("No major improvements needed!")
