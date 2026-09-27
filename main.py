from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from core.engine import DriverSynthesisEngine

load_dotenv()

app = FastAPI(title="ComponentOS Driver Synthesis Engine")
engine = DriverSynthesisEngine()

class SynthesisRequest(BaseModel):
    peripheral: str
    pinout: str

@app.post("/synthesize")
def synthesize_driver(req: SynthesisRequest):
    try:
        result = engine.synthesize(peripheral=req.peripheral, pinout=req.pinout)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "online", "system": "ComponentOS Dual-LLM Pipeline Active"}
