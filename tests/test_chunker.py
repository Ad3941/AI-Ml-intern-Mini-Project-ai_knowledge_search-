from src.chunker import chunk_text

def test_chunk_text_basic():
    sample_text = "A" * 1200
    filename = "long_doc.txt"
    chunks = chunk_text(sample_text, filename)
    
    assert len(chunks) > 1
    assert chunks[0]["source"] == filename
    assert len(chunks[0]["text"]) <= 500