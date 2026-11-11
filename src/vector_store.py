import numpy as np
from typing import List, Dict, Tuple
from src.embeddings import EmbeddingManager
from src.config import SIMILARITY_THRESHOLD, TOP_K

class VectorStore:
    def __init__(self):
        self.chunks: List[Dict[str, any]] = []
        self.embeddings: np.ndarray = np.array([])
        self.embedder = EmbeddingManager()

    def add_documents(self, new_chunks: List[Dict[str, any]]):
        if not new_chunks:
            return
        texts = [c["text"] for c in new_chunks]
        new_embeddings = self.embedder.encode(texts)
        
        self.chunks.extend(new_chunks)
        if self.embeddings.size == 0:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])

    def search(self, query: str, top_k: int = TOP_K) -> Tuple[List[Dict[str, any]], List[float]]:
        if self.embeddings.size == 0 or not self.chunks:
            return [], []
            
        query_vector = self.embedder.encode([query])[0]
        # Dot product of normalized vectors equals cosine similarity
        similarities = np.dot(self.embeddings, query_vector)
        
        top_indices = np.argsort(similarities)[::-1]
        
        results = []
        scores = []
        
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= SIMILARITY_THRESHOLD and len(results) < top_k:
                results.append(self.chunks[idx])
                scores.append(score)
                
        return results, scores

    def clear(self):
        self.chunks = []
        self.embeddings = np.array([])