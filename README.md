# 🧠 AI Note Summarizer + Document QA

A smart document analysis tool built for hackathons, allowing users to **upload PDFs or TXT files**, get **AI-powered summaries**, and ask **contextual questions** about the document — all via a simple Streamlit interface and FastAPI backend.

---

## 🚀 Features

- 📄 **PDF/TXT Upload Support**
- ✂️ **Automatic Document Summarization** using Hugging Face's `facebook/bart-large-cnn`
- 💬 **Ask Questions** based on document content (basic implementation via Hugging Face `deepset/roberta-base-squad2`)
- 🖥️ **CPU Usage Tracking**
- 🌐 **REST API-Based Architecture** for easy frontend/backend decoupling
- 🔐 **Environment Variable Support** using `.env` files
- 🐳 **Docker Support (Planned)**

---

## 🧩 Tech Stack

| Component        | Tech Used                          |
|------------------|------------------------------------|
| Frontend         | Streamlit (testing UI)             |
| Backend          | FastAPI                            |
| AI Models        | Hugging Face Transformers API      |
| File Parsing     | PyMuPDF (`fitz`)                   |
| Env Management   | python-dotenv                      |
| System Stats     | psutil                             |
| Deployment Prep  | Docker (planned)                   |

---

## 🛠️ Installation & Setup

### 🔃 Clone the repository

```bash
git clone https://github.com/JOBIN-SABU/your-repo-name.git
cd your-repo-name
