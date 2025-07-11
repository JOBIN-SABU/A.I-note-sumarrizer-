from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import fitz  
import requests
from dotenv import load_dotenv
import psutil

load_dotenv()

HF_SUMMARY_KEY = os.getenv("HF_SUMMARY_KEY")
HF_QA_KEY = os.getenv("HF_QA_KEY")

SUMMARY_MODEL = "facebook/bart-large-cnn"
QA_MODEL = "distilbert-base-cased-distilled-squad"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def summarize(text):
    api_url = f"https://api-inference.huggingface.co/models/{SUMMARY_MODEL}"
    headers = {"Authorization": f"Bearer {HF_SUMMARY_KEY}"}
    payload = {"inputs": text}
    response = requests.post(api_url, headers=headers, json=payload)

    print(">>> Summary Status Code:", response.status_code)
    print(">>> Summary Response:", response.text)

    if response.status_code != 200:
        raise Exception(f"Hugging Face summarization failed: {response.text}")
    return response.json()[0]["summary_text"]


def answer_question(question, context):
    api_url = f"https://api-inference.huggingface.co/models/{QA_MODEL}"
    headers = {"Authorization": f"Bearer {HF_QA_KEY}"}
    payload = {"question": question, "context": context}
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code != 200:
        print("⚠️ Q&A API Error:", response.text)
        raise Exception("Hugging Face Q&A failed.")

    print("🔍 QA Response JSON:", response.json())
    return response.json().get("answer", "No answer found.")



@app.post("/summarize")
async def summarize_doc(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF or TXT supported.")

    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
    finally:
        os.remove(path)

    if len(text.strip()) < 10:
        raise HTTPException(status_code=400, detail="File empty or unreadable.")

    summary = summarize(text[:1024])
    cpu = psutil.cpu_percent(interval=1)

    return {"summary": summary, "cpu_usage": cpu, "document_text": text[:3000]}

@app.post("/ask")
async def ask_question(question: str = Form(...), context: str = Form(...)):
    print("Received question:", question)
    print("Received context (first 200 chars):", context[:200])
    if len(context.strip()) < 10:
        raise HTTPException(status_code=400, detail="Invalid context.")

    try:
        answer = answer_question(question, context[:3000])
    except Exception as e:
        print("HF error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"answer": answer}


