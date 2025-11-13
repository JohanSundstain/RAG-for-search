import os
import sys

import numpy as np
import pickle
from lgbt import lgbt

from config import config
from db import texts_interface
from embedder import embedder_model
from vector_db import faiss_interface


def split_text(text: str, max_tokens: int = 1000):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i + max_tokens])


def main():
	if len(sys.argv) > 2:
		raise ValueError("Please provide user request as a command line argument")
	
	user_request = sys.argv[1] # чтение запроса пользователя из аргументов командной строки

	if os.path.exists("chunks.pkl"):
		with open("chunks.pkl", "rb") as f:
			chunks = pickle.load(f)
	else:
		chunks = []
	
	texts = texts_interface.get_all_texts()
    
	new_chunks = []
	new_embeddings = []
	for text in lgbt(texts, desc="Texts: ", mode="fra"):
		if text.pk_id not in chunks:
			for chunk in split_text(text.textt, int(config['MAX_TOKENS'])):
				new_chunks.append(text.pk_id)
				new_embeddings.append(embedder_model.get_embedding(chunk))

	if len(new_chunks) > 0: 
		np_embeddings = np.array(new_embeddings, dtype="float32")
		faiss_interface.add(np_embeddings)
		faiss_interface.save()
		chunks.extend(new_chunks)
		pickle.dump(chunks, open("chunks.pkl", "wb"))

	user_request_embedding = np.array(embedder_model.get_embedding(user_request))
	index = faiss_interface.search(user_request_embedding)

	for idx in index:
		print(chunks[idx])


if __name__ == "__main__":
    main()
