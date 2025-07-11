import streamlit as st
import requests

st.set_page_config(page_title="AI Note Summarizer + QA", layout="wide")
st.title("📄 AI Note Summarizer with Document QA")

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    st.info("⏳ Uploading and summarizing document...")
    files = {"file": (uploaded_file.name, uploaded_file.read())}

    try:
        res = requests.post("http://localhost:8000/summarize", files=files)
        data = res.json()

        if res.status_code == 200:
            st.success("✅ Summary generated!")
            st.subheader("📄 Summary")
            st.text_area("Summary Output", data["summary"], height=250)
            st.caption(f"🖥️ CPU Usage: {data['cpu_usage']}%")

            with st.expander("📝 Ask a Question about the Document"):
                question = st.text_input("Enter your question")
                if st.button("Get Answer") and question:
                    try:
                        qa_res = requests.post(
                            "http://localhost:8000/ask",
                            data={
                                "question": question,
                                "context": data["document_text"]
                            }
                        )
                        qa_data = qa_res.json()
                        answer = qa_data.get("answer", "No answer found.")
                        st.success(f"💬 Answer: {answer}")
                    except Exception as e:
                        st.error(f"❌ QA Error: {e}")

        else:
            st.error(f"❌ {data.get('detail', 'Unknown error')}")

    except Exception as e:
        st.error(f"❌ Backend Error: {e}")
