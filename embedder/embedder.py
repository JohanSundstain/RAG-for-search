from openai import OpenAI
from config import config

class Embedder:
	def __init__(self):
		self.client = OpenAI(api_key=config['API_KEY'])

	def get_embedding(self, text: str):
		response = self.client.embeddings.create(
			model=config['EMBEDDING_MODEL'],  # или text-embedding-3-small
			input=text
		)
		embedding = response.data[0].embedding
		return embedding