import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from embeddings import EmbeddingService
from document_store import DocumentStore
from rag_workflow import RagWorkflow

app = FastAPI(title="Learning RAG Demo")

embed_service = EmbeddingService(dim=128)
doc_store = DocumentStore(vector_size=128, collection_name="demo_collection")
rag = RagWorkflow(embedder=embed_service, store=doc_store)

class QuestionRequest(BaseModel):
    question: str

class DocumentRequest(BaseModel):
    text: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    start = time.time()
    try:
        result = rag.run(req.question)
        return {
            "question": req.question,
            "answer": result.get("answer"),
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add")
def add_document(req: DocumentRequest):
    try:
        emb = embed_service.embed(req.text)
        doc_id = doc_store.add_document(req.text, vector=emb)
        return {"id": doc_id, "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
def status():
    return {
        "qdrant_ready": doc_store.using_qdrant,
        "in_memory_docs_count": doc_store.in_memory_count(),
        "graph_ready": True  
    }
