import pytest
from src.vector_store import VectorStore

def test_vector_store_search():
    store = VectorStore()
    chunks = [
        {"text": "Python is a programming language created by Guido van Rossum.", "source": "python.txt", "start_idx": 0, "end_idx": 50},
        {"text": "Acme Corp requires full-disk encryption on all laptops.", "source": "policy.md", "start_idx": 0, "end_idx": 50}
    ]
    store.add_documents(chunks)
    
    results, scores = store.search("Who created Python?", top_k=1)
    assert len(results) == 1
    assert "Guido van Rossum" in results[0]["text"]