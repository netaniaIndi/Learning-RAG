from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class DocumentStore:
    def __init__(self, vector_size= 128, collection_name= "demo_collection"):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._use_qdrant = False
        self._qdrant = None
        self._in_memory = []
        self._next_id = 0

        try:
            self._qdrant = QdrantClient("http://localhost:6333")
            self._qdrant.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
            self._use_qdrant = True
        except Exception:
            print("⚠️  Qdrant not available. Falling back to in-memory list.")
            self._use_qdrant = False

    @property
    def using_qdrant(self):
        return self._use_qdrant

    def add_document(self, doc_text, vector= None):
        doc_id = self._next_id
        self._next_id += 1

        if self._use_qdrant and vector is not None:
            payload = {"text": doc_text}
            point = PointStruct(id=doc_id, vector=vector, payload=payload)
            self._qdrant.upsert(collection_name=self.collection_name, points=[point])
        else:
            self._in_memory.append(doc_text)
        return doc_id

    def retrieve_by_query_text(self, query, query_vector= None, limit= 2):
        results = []
        if self._use_qdrant and query_vector is not None:
            hits = self._qdrant.search(collection_name=self.collection_name, query_vector=query_vector, limit=limit)
            for hit in hits:
                payload = hit.payload or {}
                text = payload.get("text")
                if text:
                    results.append(text)
        else:
            q_lower = query.lower()
            for doc in self._in_memory:
                if q_lower in doc.lower():
                    results.append(doc)
            if not results and self._in_memory:
                results = [self._in_memory[0]]
        return results

    def in_memory_count(self):
        return len(self._in_memory)
