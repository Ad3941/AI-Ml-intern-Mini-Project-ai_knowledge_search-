from typing import List, Dict
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str, filename: str) -> List[Dict[str, any]]:
    """Splits text into overlapping chunks with metadata."""
    if not text.strip():
        return []
        
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + CHUNK_SIZE
        chunk_str = text[start:end]
        
        # Clean up whitespace
        chunk_str = " ".join(chunk_str.split())
        
        if chunk_str:
            chunks.append({
                "text": chunk_str,
                "source": filename,
                "start_idx": start,
                "end_idx": min(end, text_len)
            })
            
        if end >= text_len:
            break
            
        start += CHUNK_SIZE - CHUNK_OVERLAP
        
    return chunks