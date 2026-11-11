# AI Knowledge Search Tool

A modular Python web application built with Streamlit that enables users to upload local documents (`.txt`, `.md`, `.pdf`, `.docx`), index them via local sentence embeddings, perform semantic vector search, and generate grounded answers with source citations.

---

## Architecture & Flow

```mermaid
graph TD
    A[Upload Files: txt, md, pdf, docx] --> B[Text Extractor]
    B --> C[Overlapping Chunker (~500 chars)]
    C --> D[Embedding Model: all-MiniLM-L6-v2]
    D --> E[(In-Memory Vector Store)]
    
    F[User Question] --> G[Query Encoder]
    G --> H[Cosine Similarity Search]
    E --> H
    H --> I{API Key Configured?}
    I -->|Yes| J[LLM Generation OpenAI / Anthropic]
    I -->|No| K[Extractive Fallback Mode]
    J --> L[Display Answer + Sources]
    K --> L