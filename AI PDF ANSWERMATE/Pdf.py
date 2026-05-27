#import
from mistralai import Mistral
from dotenv import load_dotenv
import os 
load_dotenv()
client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
    )
from PyPDF2 import PdfReader
#load pdf
reader = PdfReader("sample1.pdf")
# show text
for i , page in enumerate(reader.pages):
    text=page.extract_text()
    print(f"--page{i+1}--")
#split question 
lines = text.split("\n")
questions = []
for line in lines :
    line = line.strip()
    for i,h in enumerate(lines):
        if line.startswith(str(i) + "."):
            q = line.split(".",1)[1].strip()
   
            questions.append(q)

# Use AI
# import requests
# url = "http://localhost:11434/api/generate"
# print("Making....")
for i,pro in enumerate(questions):
    prompt = f"""
    Question: {pro}
    Write a clear, well-structured answer with 10 key points,
    examples, and conclusion  using
    English style for easy understanding.
    """
    print(f"{i+1}. {pro}")
    # response = requests.post(
    #     url,
    #     json={
    #         "model": "llama3.2",
    #         "prompt": prompt,
    #         "stream": False
    #     }
    # )
    # data = response.json()['response']

    # print(data)    
    ####USE MISTRAL API 
   
    response = client.chat.complete(
        model="ministral-3b-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    opt= response.choices[0].message.content
    with open("answers.txt", "w",encoding="utf-8") as file:
        file.write(pro + "\n" + opt)  