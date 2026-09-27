from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.engine import ComponentOSEngine

app = FastAPI(title="ComponentOS API")
engine = ComponentOSEngine()

class DriverRequest(BaseModel):
    peripheral: str
    pinout: str

@app.post("/synthesize")
def synthesize(request: DriverRequest):
    try:
        code = engine.synthesize_driver(request.peripheral, request.pinout)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}
