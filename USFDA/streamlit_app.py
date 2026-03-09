import streamlit as st
import os
import fitz
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

st.title("FDA Drug Information & Document Chat")

if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False


# ---------------------------
# PDF CHAT FUNCTIONS
# ---------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks


def build_index(chunks):
    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index


def search_question(question, index, chunks):

    q_embedding = model.encode([question])

    distances, indices = index.search(np.array(q_embedding), 3)

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


# ---------------------------
# UI SECTION
# ---------------------------

st.header("Chat with FDA Review Documents")

pdf_files = os.listdir("documents")

if len(pdf_files) == 0:
    st.warning("No PDFs found in the documents folder.")
else:

    selected_pdf = st.selectbox("Select a document", pdf_files)

    pdf_path = os.path.join("documents", selected_pdf)

    if st.button("Load Document"):

        with st.spinner("Reading PDF..."):
            text = extract_text_from_pdf(pdf_path)
            chunks = chunk_text(text)
            index = build_index(chunks)

        st.session_state.chunks = chunks
        st.session_state.index = index
        st.session_state.doc_loaded = True


    if st.session_state.doc_loaded:

        st.success("Document loaded!")
        
        question = st.text_input("Ask a question about the document")

        if question:
            
            results = search_question(
                question,
                st.session_state.index,
                st.session_state.chunks
                )

            st.subheader("Relevant Sections")

            for r in results:
                st.write(r[:400])
                st.write("---")