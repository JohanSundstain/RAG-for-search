from .faiss_db import FaissDB
from config import config

embedder_name = config["EMBEDDING_MODEL"]
dim = 1536 if embedder_name == "text-embedding-3-small" else 3072
faiss_interface = FaissDB(dim=dim)

__all__ = [faiss_interface]