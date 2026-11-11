import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL_NAME

class EmbeddingManager:
    _instance = None
    _model = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        return cls._model

    def encode(self, texts: list[str]) -> np.ndarray:
        """Generates L2-normalized embeddings for similarity computations."""
        model = self.get_model()
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # Normalize for cosine similarity via dot product
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1e-10
        return embeddings / norms