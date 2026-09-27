from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from core.engine import DriverSynthesisEngine
from core.deployer import flash_to_microcontroller

load_dotenv()

app = FastAPI(title="ComponentOS Universal Microcontroller Synthesis & Deployment Engine")
engine = DriverSynthesisEngine()

class SynthesisRequest(BaseModel):
    peripheral: str
    pinout: str
    target: str = "esp32"  # e.g., esp32, rp2040, stm32
    flash: bool = False
    port: str = None       # e.g., /dev/ttyUSB0, /dev/ttyACM0, COM3

@app.post("/synthesize", summary="Synthesize and deploy driver to any MicroPython target")
def synthesize_driver(req: SynthesisRequest):
    try:
        # Step 1-3: Plan, Code, and Validate
        result = engine.synthesize(peripheral=req.peripheral, pinout=req.pinout, target=req.target)
        
        # Step 4: Universal Flash
        if req.flash:
            deployment_status = flash_to_microcontroller(
                code=result["code"], 
                target=req.target,
                filename=f"{req.peripheral.split()[0].lower()}.py", 
                port=req.port
            )
            result["deployment"] = deployment_status
            
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
