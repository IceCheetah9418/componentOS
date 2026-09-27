from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from core.engine import DriverSynthesisEngine

load_dotenv()

app = FastAPI(
    title="ComponentOS Driver Synthesis Engine",
    description="Autonomous MicroPython driver synthesis pipeline for ESP32 utilizing dual-LLM architecture and AST security validation.",
    version="1.0.0"
)

engine = DriverSynthesisEngine()

class SynthesisRequest(BaseModel):
    peripheral: str
    pinout: str

@app.post("/synthesize", summary="Synthesize and validate a hardware driver")
def synthesize_driver(req: SynthesisRequest):
    try:
        result = engine.synthesize(peripheral=req.peripheral, pinout=req.pinout)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health", summary="System health check")
def health_check():
    return {"status": "online", "system": "ComponentOS Dual-LLM Pipeline Active"}
