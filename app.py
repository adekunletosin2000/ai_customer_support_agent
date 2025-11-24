from fastapi import FastAPI
from orchestrator import run_orchestration
app=FastAPI()
@app.post("/orchestrate")
async def orchestrate(payload:dict):
    return run_orchestration(payload.get("message",""))
