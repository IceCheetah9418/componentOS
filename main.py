import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from core.engine import DriverSynthesisEngine

# Safe import for deployer with graceful fallback
try:
    from core.deployer import flash_to_microcontroller
    DEPLOYER_AVAILABLE = True
except ImportError:
    DEPLOYER_AVAILABLE = False

load_dotenv()

app = FastAPI(
    title="ComponentOS Universal Microcontroller Synthesis & Deployment Engine",
    description="Autonomous MicroPython driver synthesis pipeline utilizing dual-LLM architecture and AST security validation.",
    version="1.0.1"
)

engine = DriverSynthesisEngine()

SUPPORTED_TARGETS = {"esp32", "rp2040", "stm32"}

class SynthesisRequest(BaseModel):
    peripheral: str = Field(..., min_length=1, description="Name of the peripheral component")
    pinout: str = Field(..., min_length=1, description="Physical pin mapping configuration")
    target: str = Field("esp32", description="Microcontroller target architecture")
    flash: bool = Field(False, description="Whether to flash the code to the target device")
    port: str = Field(None, description="Serial port path (e.g., /dev/ttyUSB0, COM3)")

@app.post("/synthesize", summary="Synthesize and deploy driver to any MicroPython target")
def synthesize_driver(req: SynthesisRequest):
    # 1. Validate target architecture
    target_lower = req.target.lower()
    if target_lower not in SUPPORTED_TARGETS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported target '{req.target}'. Supported targets: {list(SUPPORTED_TARGETS)}"
        )

    # 2. Safe string manipulation for filename generation
    cleaned_peripheral = req.peripheral.strip()
    if not cleaned_peripheral:
        raise HTTPException(status_code=400, detail="Peripheral description cannot be empty.")
    filename = f"{cleaned_peripheral.split()[0].lower()}.py"

    # 3. Validate serial port and deployer availability if flashing is requested
    if req.flash:
        if not DEPLOYER_AVAILABLE:
            raise HTTPException(status_code=500, detail="Deployment module is not available on this server instance.")
        if not req.port:
            raise HTTPException(status_code=400, detail="A serial port must be provided when flash=True.")
        if req.port.startswith("/dev/") and not os.path.exists(req.port):
            raise HTTPException(status_code=400, detail=f"Specified serial port '{req.port}' does not exist on the host system.")

    try:
        # Step 1-3: Plan, Code, and Validate via LLM Engine
        result = engine.synthesize(peripheral=req.peripheral, pinout=req.pinout, target=target_lower)

        # Step 4: Universal Flash with isolated error handling
        if req.flash:
            try:
                deployment_status = flash_to_microcontroller(
                    code=result["code"],
                    target=target_lower,
                    filename=filename,
                    port=req.port
                )
                result["deployment"] = deployment_status
            except Exception as deploy_err:
                raise HTTPException(
                    status_code=502, 
                    detail=f"Driver synthesized successfully, but hardware deployment failed: {str(deploy_err)}"
                )

        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synthesis engine error: {str(e)}")

@app.get("/health", summary="System health check")
def health_check():
    return {
        "status": "online",
        "system": "ComponentOS Dual-LLM Pipeline Active",
        "deployer_available": DEPLOYER_AVAILABLE
    }
