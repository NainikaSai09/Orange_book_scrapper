# USFDA Knowledge Mining Tool

## Overview

The **USFDA Knowledge Mining Tool** is a Python-based system designed to extract and query regulatory drug information from official FDA sources. The tool enables users to retrieve drug product details, patent information, and regulatory documentation through automated data extraction and semantic document search.

The system focuses on the **US pharmaceutical market**, specifically using:

* **FDA Orange Book** – Approved Drug Products with Therapeutic Equivalence Evaluations
* **Drugs@FDA** – FDA Approved Drugs database

The solution combines **web scraping, document processing, vector embeddings, and semantic search** to allow users to ask questions and retrieve relevant information from regulatory datasets and review documents.

The current implementation demonstrates the workflow using the molecule **Proamatine** as a proof-of-concept.

---

# Project Objective

The objective of this project is to build a **knowledge mining solution** capable of:

* Extracting relevant drug regulatory data from official databases
* Processing regulatory documents such as FDA review PDFs
* Allowing users to query specific questions
* Returning relevant answers from extracted sources

The tool demonstrates how regulatory information across multiple datasets can be integrated into a searchable knowledge system.

---

# Data Sources

The assignment specifies several regulatory sources across global markets.
This implementation focuses on **US Market sources**.

### United States

**1. Orange Book**

* Approved Drug Products with Therapeutic Equivalence Evaluations
* Provides product, patent, and exclusivity data

**2. Drugs@FDA**

* FDA Approved Drug database
* Provides regulatory documentation including review letters, labels, and approval information

For the molecule **Proamatine**, the following Orange Book datasets were used:

* `products.txt`
* `patent.txt`
* `exclusivity.txt`

Additionally, the FDA review document:

```
proamatine_review.pdf
```

was used for document-based querying.

---

# System Architecture

The system consists of three major components:

1. **Data Extraction Layer**
2. **Document Knowledge Mining Layer**
3. **User Interaction Layer**

```
User Query
     │
     ▼
Streamlit Web Interface
     │
     ▼
PDF Processing & Embedding Generation
     │
     ▼
Vector Index (FAISS)
     │
     ▼
Semantic Similarity Search
     │
     ▼
Relevant Document Sections Returned
```

---

# Project Structure

```
USFDA/
│
├── documents/
│   └── proamatine_review.pdf
│
├── src/
│   ├── documents/
│   │   └── pdf_chat.py
│   │
│   ├── orangebook/
│   │   ├── orangebook_scrapper.py
│   │   ├── exclusivity.txt
│   │   ├── patent.txt
│   │   ├── products.txt
│   │   └── test_bs4.py
│   │
│   └── utils/
│
├── streamlit_app.py
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# Core Components

## 1. Orange Book Scraper

**File:**
`src/orangebook/orangebook_scrapper.py`

This module extracts regulatory drug information from Orange Book datasets.

### Functionality

* Reads Orange Book data files:

  * `products.txt`
  * `patent.txt`
  * `exclusivity.txt`
* Allows users to input a drug name
* Returns structured information related to:

  * Product details
  * Patent information
  * Market exclusivity

Example query:

```
Enter product name: Proamatine
```

The tool retrieves and displays relevant regulatory information for the drug.

---

## 2. Document Knowledge Mining (PDF Chat)

**File:**
`src/documents/pdf_chat.py`

This module enables **semantic search across FDA review documents**.

### Workflow

1. Load FDA review PDF
2. Extract text from the document
3. Split the text into smaller chunks
4. Generate embeddings for each chunk
5. Store embeddings in a FAISS vector index
6. Compare user questions with stored embeddings
7. Return the most relevant sections

This allows users to query regulatory documents such as:

```
What is the active ingredient in Proamatine?
```

and retrieve relevant portions of the review document.

---

## 3. Streamlit Interface

**File:**
`streamlit_app.py`

This module provides a **web interface for interacting with regulatory documents**.

### Features

* Upload or select a regulatory document
* Load and process the document
* Ask natural language questions
* Retrieve relevant information from the document

The Streamlit application creates a simple interactive interface where users can:

1. Load an FDA review PDF
2. Ask questions about the document
3. View relevant extracted sections

---

# Knowledge Mining Pipeline

The system performs knowledge extraction through the following pipeline:

### Step 1 — Data Acquisition

Regulatory datasets are obtained from:

* Orange Book datasets
* FDA review documents

### Step 2 — Document Parsing

PDF files are processed using **PyMuPDF (fitz)** to extract textual content.

### Step 3 — Text Chunking

Large documents are divided into smaller text segments to enable efficient processing.

### Step 4 — Embedding Generation

Each text chunk is converted into vector embeddings using:

```
Sentence Transformers
Model: all-MiniLM-L6-v2
```

### Step 5 — Vector Indexing

Embeddings are stored in a **FAISS similarity index** to support fast semantic search.

### Step 6 — Query Processing

User queries are embedded and compared against the indexed vectors.

### Step 7 — Result Retrieval

The most relevant document sections are returned to the user.

---

# Technology Stack

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Core programming language |
| Streamlit             | Web interface             |
| PyMuPDF               | PDF text extraction       |
| Sentence Transformers | Text embeddings           |
| FAISS                 | Vector similarity search  |
| NumPy                 | Numerical processing      |

---

# Installation

Clone the repository:

```bash
git clone https://github.com/NainikaSai09/Orange_book_scrapper.git
cd USFDA
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application will open in a browser at:

```
http://localhost:8501
```

---

# Example Usage

1. Launch the Streamlit interface
2. Select the FDA review document
3. Click **Load Document**
4. Ask a question about the drug

Example questions:

```
What is Proamatine used for?
What is the active ingredient?
What are the pharmacological properties?
```

The system returns the most relevant sections from the review document.

---

# Current Scope

This implementation demonstrates the knowledge mining workflow using:

* **One molecule:** Proamatine
* **One FDA review document**
* **Orange Book datasets for the same drug**

The project serves as a **proof-of-concept for automated regulatory knowledge extraction**.

# Author

Nainika Neerukonda

