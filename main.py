import os
import logging
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.middleware.base import BaseHTTPMiddleware
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ComponentOS Universal Microcontroller Synthesis & Deployment Engine",
    description="Autonomous MicroPython driver synthesis pipeline utilizing dual-LLM architecture and AST security validation.",
    version="1.0.2"
)

engine = DriverSynthesisEngine()

SUPPORTED_TARGETS = {"esp32", "rp2040", "stm32"}

class SynthesisRequest(BaseModel):
    peripheral: str = Field(..., min_length=1, description="Name of the peripheral component")
    pinout: str = Field(..., min_length=1, description="Physical pin mapping configuration")
    target: str = Field("esp32", description="Microcontroller target architecture")
    flash: bool = Field(False, description="Whether to flash the code to the target device")
    port: str = Field(None, description="Serial port path (e.g., /dev/ttyUSB0, COM3)")

# Rate limiting middleware (simple in-memory tracker)
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # api_key -> [(timestamp, count)]

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/synthesize":
            api_key = request.headers.get("x-api-key", "anonymous")
            now = datetime.now().timestamp()
            
            if api_key not in self.requests:
                self.requests[api_key] = []
            
            # Clean old entries
            self.requests[api_key] = [
                t for t in self.requests[api_key]
                if now - t < self.window_seconds
            ]
            
            if len(self.requests[api_key]) >= self.max_requests:
                logger.warning(f"Rate limit exceeded for {api_key}")
                raise HTTPException(status_code=429, detail="Rate limit exceeded. Max 10 requests per minute.")
            
            self.requests[api_key].append(now)
        
        response = await call_next(request)
        return response

app.add_middleware(RateLimitMiddleware)

def verify_api_key(x_api_key: str = Header(None)) -> str:
    """Verify API key from request header."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required. Use header: x-api-key")
    
    # In production, validate against database
    expected_key = os.getenv("API_KEY")
    if expected_key and x_api_key != expected_key:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return x_api_key

@app.post("/synthesize", summary="Synthesize and deploy driver to any MicroPython target")
def synthesize_driver(req: SynthesisRequest, api_key: str = Depends(verify_api_key)):
    """Synthesize a driver for a peripheral and optionally flash to device."""
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Synthesis request: {req.peripheral} for {req.target}")
    
    try:
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
                raise HTTPException(status_code=400, detail=f"Specified serial port does not exist.")

        # Step 1-3: Plan, Code, and Validate via LLM Engine
        logger.info(f"[{request_id}] Running synthesis engine")
        result = engine.synthesize(peripheral=req.peripheral, pinout=req.pinout, target=target_lower)

        # Step 4: Universal Flash with isolated error handling
        if req.flash:
            try:
                logger.info(f"[{request_id}] Deploying to {target_lower}")
                deployment_status = flash_to_microcontroller(
                    code=result["code"],
                    target=target_lower,
                    filename=filename,
                    port=req.port
                )
                result["deployment"] = deployment_status
                logger.info(f"[{request_id}] Deployment successful")
            except Exception as deploy_err:
                logger.error(f"[{request_id}] Deployment failed: {type(deploy_err).__name__}")
                raise HTTPException(
                    status_code=502, 
                    detail=f"Driver synthesized successfully, but hardware deployment failed. {str(deploy_err)}"
                )

        logger.info(f"[{request_id}] Synthesis completed successfully")
        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error: {type(e).__name__}: {str(e)[:200]}")
        raise HTTPException(status_code=500, detail="An internal error occurred during synthesis. Please try again.")

@app.get("/health", summary="System health check")
def health_check():
    return {
        "status": "online",
        "system": "ComponentOS Dual-LLM Pipeline Active",
        "deployer_available": DEPLOYER_AVAILABLE
    }
