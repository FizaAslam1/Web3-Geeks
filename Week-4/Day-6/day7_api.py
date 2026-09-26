"""
Day 7 — FastAPI backend for RealEstate Voice Agent
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os, json
from datetime import datetime

app = FastAPI(title="RealEstate Hub Voice Agent", version="1.0.0")

# ---- In-memory metrics (replace with real logging in production) ----
METRICS = {
    "total_requests": 0,
    "errors": 0,
    "started_at": datetime.now().isoformat(),
}


class ChatRequest(BaseModel):
    message: str
    user_phone: Optional[str] = "0300-0000000"


class ChatResponse(BaseModel):
    response: str
    intent: str
    latency_s: float


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_metrics": METRICS,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Chat endpoint. Day 7 will wire this to the LangGraph agent.
    For now, returns a placeholder.
    """
    METRICS["total_requests"] += 1
    t0 = datetime.now()

    # TODO Day 7: wire to `app.invoke(initial_state(req.message, req.user_phone))`
    response_text = "Placeholder: agent not wired yet."

    latency = (datetime.now() - t0).total_seconds()
    return ChatResponse(response=response_text, intent="placeholder", latency_s=latency)


@app.get("/metrics")
def metrics():
    return METRICS
