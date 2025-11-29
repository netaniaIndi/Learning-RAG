from embeddings import EmbeddingService
from document_store import DocumentStore

class RagWorkflow:
    def __init__(self, embedder: EmbeddingService, store: DocumentStore):
        self.embedder = embedder
        self.store = store

    def retrieve(self, question: str):
        state = {"question": question}
        emb = self.embedder.embed(question)
        results = self.store.retrieve_by_query_text(question, query_vector=emb, limit=2)
        state["context"] = results
        return state

    def answer(self, state):
        ctx = state.get("context", [])
        if ctx:
            answer = f"I found this: '{ctx[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        state["answer"] = answer
        return state

    def run(self, question: str):
        s = self.retrieve(question)
        s = self.answer(s)
        return s
