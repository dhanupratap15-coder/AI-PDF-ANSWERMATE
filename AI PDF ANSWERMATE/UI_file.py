
import streamlit as st
from mistralai import Mistral
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os

# Load API Key
load_dotenv()

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

# Page Config
st.set_page_config(
    page_title="AI PDF AnswerMate",
    page_icon="📘",
    layout="wide"
)

# Title
st.title("📘 AI PDF AnswerMate")
st.write("Upload a PDF containing questions and generate AI answers automatically.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload PDF File",
    type=["pdf"]
)

# Function to extract questions
def extract_questions(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    lines = text.split("\n")

    questions = []

    for line in lines:
        line = line.strip()

        if line:
            for i in range(1, 100):
                if line.startswith(f"{i}."):
                    q = line.split(".", 1)[1].strip()
                    questions.append(q)

    return questions

# Generate Answers
if uploaded_file:

    st.success("PDF Uploaded Successfully!")

    questions = extract_questions(uploaded_file)

    st.write(f"### Total Questions Found: {len(questions)}")

    if st.button("Generate Answers"):

        all_answers = ""

        for i, question in enumerate(questions):

            with st.spinner(f"Generating answer for Question {i+1}..."):

                prompt = f"""
                Question: {question}

                Write a clear, well-structured answer with:
                - 10 key points
                - Examples
                - Conclusion
                Use simple English for easy understanding.
                """

                response = client.chat.complete(
                    model="mistral-small-latest",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = response.choices[0].message.content

                st.subheader(f"Question {i+1}")
                st.write(question)

                st.subheader("Answer")
                st.write(answer)

                st.markdown("---")

                all_answers += f"\n\nQuestion {i+1}: {question}\n\n"
                all_answers += f"{answer}\n"
                all_answers += "="*80

        # Download Button
        st.download_button(
            label="📥 Download Answers",
            data=all_answers,
            file_name="answers.txt",
            mime="text/plain"
        )