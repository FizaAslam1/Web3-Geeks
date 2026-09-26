from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json, time
from agent_core import run_agent

app = FastAPI(title="RealEstate Hub Voice Agent API", version="1.0")

class ChatRequest(BaseModel):
    user_input: str
    user_phone: str = "0300-0000000"

class ChatResponse(BaseModel):
    intent: str
    response: str
    latency_s: float

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    t0 = time.time()
    result = run_agent(req.user_input, req.user_phone)
    latency = time.time() - t0
    return ChatResponse(intent=result.get("intent", "unknown"),
                         response=result.get("response", ""), latency_s=round(latency, 3))

@app.get("/metrics")
def metrics():
    events = []
    try:
        with open("day6_monitoring_log.jsonl") as f:
            events = [json.loads(l) for l in f]
    except FileNotFoundError:
        pass
    return {"total_calls_logged": len(events), "recent": events[-10:]}
