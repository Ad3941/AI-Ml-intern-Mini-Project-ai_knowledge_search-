import streamlit as st
from src.loader import load_file
from src.chunker import chunk_text
from src.vector_store import VectorStore
from src.qa import generate_answer
from src.config import TOP_K, SIMILARITY_THRESHOLD

st.set_page_config(page_title="AI Knowledge Search Tool", page_icon="📚", layout="wide")

# Initialize Vector Store in session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = {}

st.title("📚 AI Knowledge Search Tool")
st.markdown("Upload documents, index them instantly, and perform semantic search with source grounding.")

with st.sidebar:
    st.header("1. Document Ingestion")
    uploaded_files = st.file_uploader(
        "Upload files (.txt, .md, .pdf, .docx)",
        type=["txt", "md", "pdf", "docx"],
        accept_multiple_files=True
    )
    
    if st.button("Process & Index Documents", type="primary"):
        if uploaded_files:
            st.session_state.vector_store.clear()
            st.session_state.indexed_files = {}
            
            total_chunks = 0
            for file in uploaded_files:
                try:
                    file_bytes = file.read()
                    text = load_file(file_bytes, file.name)
                    chunks = chunk_text(text, file.name)
                    if chunks:
                        st.session_state.vector_store.add_documents(chunks)
                        st.session_state.indexed_files[file.name] = len(chunks)
                        total_chunks += len(chunks)
                except Exception as e:
                    st.error(f"Failed to process {file.name}: {e}")
            
            st.success(f"Successfully indexed {len(st.session_state.indexed_files)} files ({total_chunks} total chunks).")
        else:
            st.warning("Please upload at least one file first.")

    if st.session_state.indexed_files:
        st.divider()
        st.subheader("Indexed Files Summary")
        for filename, count in st.session_state.indexed_files.items():
            st.text(f"• {filename}: {count} chunks")

# Main Interface: Question Answering
st.header("2. Ask Questions")
query = st.text_input("Enter your natural language question:")

if st.button("Search & Answer"):
    if not st.session_state.indexed_files:
        st.warning("Please upload and index documents in the sidebar before searching.")
    elif not query.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Searching knowledge base..."):
            results, scores = st.session_state.vector_store.search(query, top_k=TOP_K)
            answer, mode = generate_answer(query, results, scores)
            
            st.subheader("Answer")
            st.markdown(answer)
            st.caption(f"Generation mode: `{mode}` | Threshold: `{SIMILARITY_THRESHOLD}`")
            
            st.divider()
            st.subheader("Supporting Sources & Chunks")
            if not results:
                st.info("No matching chunks found above the similarity threshold.")
            else:
                for i, (chunk, score) in enumerate(zip(results, scores)):
                    with st.expander(f"Source {i+1}: {chunk['source']} (Similarity: {score:.4f})"):
                        st.markdown(f"**Chunk Text:**\n> {chunk['text']}")