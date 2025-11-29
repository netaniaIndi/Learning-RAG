import random

class EmbeddingService:
    def __init__(self, dim: int = 128):
        self.dim = dim

    def embed(self, text: str): 
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.dim)]
