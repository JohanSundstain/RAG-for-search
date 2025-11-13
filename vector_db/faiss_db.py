import os

import numpy as np
import pickle
import faiss
import hashlib

class FaissDB:
    def __init__(self, dim: int):
        if os.path.exists("faiss_index.index"):
            self.index = faiss.read_index("faiss_index.index")
        else:
            self.index = faiss.IndexFlatL2(dim)
            
    def _get_key(self, array: np.ndarray):
        return hashlib.sha256(array.tobytes()).hexdigest()

    def add(self, vectors: np.ndarray):
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)
        self.index.add(vectors.astype("float32"))

    def search(self, query_vector: np.ndarray, k: int = 4) -> list[int]:
        _, I = self.index.search(query_vector.reshape(1, -1).astype("float32"), k)
        return I[0].tolist()

    def save(self):
        faiss.write_index(self.index, "faiss_index.index")
