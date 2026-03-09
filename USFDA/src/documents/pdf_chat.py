import fitz
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def chunk_text(text, chunk_size=500):
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

    return index, embeddings


def search_question(question, index, chunks):
    q_embedding = model.encode([question])

    distances, indices = index.search(np.array(q_embedding), 3)

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


def chat_with_pdf(pdf_path):
    print("\nLoading PDF...")

    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    index, embeddings = build_index(chunks)

    print("PDF loaded. You can now ask questions.\n")

    while True:
        question = input("Ask question (or type exit): ")

        if question.lower() == "exit":
            break

        results = search_question(question, index, chunks)

        print("\nRelevant answer sections:\n")

        for r in results:
            print("\nPossible answer:")
            print(r.strip()[:300])
            print("\n----------------\n")


if __name__ == "__main__":
    pdf_path = input("Enter PDF path: ")
    chat_with_pdf(pdf_path)