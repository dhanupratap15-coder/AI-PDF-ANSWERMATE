import streamlit as st
from mistralai import Mistral
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from docx import Document
import tempfile
import os

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="SmartDocs AI",
    page_icon="📚",
    layout="wide"
)

# =====================
# LOAD API
# =====================
load_dotenv()

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.title("🚀 SmartDocs AI")

    st.markdown("### Upcoming Features")

    st.info("""
    1. 📊 Excel Support
    2. 📽️ PowerPoint Support
    3. 🤖 AI Assistant Chat
    4. ⚙️ Custom AI Models
    5. 📝 Detailed Answers
    6. 🎓 Study Mode
    7. 📤 Export Options
    8. 🌙 Dark Mode
    9. 🔍 Semantic Search
    10. 📚 Multi Document Analysis
    """)

# =====================
# TITLE
# =====================
st.title("📚 SmartDocs AI")
st.caption("Upload Documents and Get AI-Powered Insights")

# =====================
# FILE UPLOAD
# =====================
uploaded_file = st.file_uploader(
    "Upload your file",
    type=["pdf", "docx", "txt"]
)

reader = ""

# =====================
# LOAD FILE
# =====================
if uploaded_file:

    suffix = "." + uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    file_type = uploaded_file.name.split(".")[-1].lower()

    try:
        if file_type == "pdf":
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            reader = "\n".join([doc.page_content for doc in docs])

        elif file_type == "docx":
            loader = Docx2txtLoader(temp_path)
            docs = loader.load()
            reader = docs[0].page_content

        elif file_type == "txt":
            loader = TextLoader(temp_path)
            docs = loader.load()
            reader = docs[0].page_content

        st.success("✅ File Loaded Successfully")

    except Exception as e:
        st.error(f"Error: {e}")

# =====================
# OPTIONS
# =====================
if reader:

    option = st.selectbox(
        "Choose Action",
        [
            "Summary",
            "Answer Questions",
            "Ask Questions"
        ]
    )

    # =====================
    # SUMMARY
    # =====================
    if option == "Summary":

        if st.button("Generate Summary"):

            with st.spinner("Generating Summary..."):

                prompt = f"""
                Summarize the following content clearly:

                {reader}
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

                result = response.choices[0].message.content

                st.subheader("📄 Summary")
                st.write(result)

    # =====================
    # ANSWER QUESTIONS
    # =====================
    elif option == "Answer Questions":

        if st.button("Generate Answers"):

            lines = reader.split("\n")
            questions = []

            for line in lines:
                line = line.strip()

                if line and line[0].isdigit():
                    try:
                        q = line.split(".", 1)[1].strip()
                        questions.append(q)
                    except:
                        pass

            if len(questions) == 0:
                st.warning("No numbered questions found.")
            else:

                for i, q in enumerate(questions):

                    with st.spinner(f"Answering Q{i+1}"):

                        prompt = f"""
                        Question: {q}

                        Write a detailed answer with:
                        - Explanation
                        - Key Points
                        - Example
                        - Conclusion
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

                        st.subheader(f"Q{i+1}. {q}")
                        st.write(answer)

                        st.divider()

    # =====================
    # ASK QUESTIONS
    # =====================
    elif option == "Ask Questions":

        user_question = st.text_input(
            "Ask anything from document"
        )

        if st.button("Ask AI") and user_question:

            with st.spinner("Thinking..."):

                prompt = f"""
                Based on this document answer:

                Question:
                {user_question}

                Document:
                {reader}
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

                st.subheader("🤖 AI Answer")
                st.write(answer)

# =====================
# FOOTER
# =====================
st.markdown("---")
st.caption('''📞 +91-7668626263  
            ✉️ dhanupratap15@gmail.com
           
            LinkedIn: linkedin.com/in/dhanu-pratap-65b913383
           

             GitHub: github.com/dhanupratap15-coder
''')