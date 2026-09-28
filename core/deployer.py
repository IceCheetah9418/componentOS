import subprocess
import os
import logging

logger = logging.getLogger(__name__)

def flash_to_microcontroller(code: str, target: str, filename: str = None, port: str = None) -> dict:
    """Flash validated code to microcontroller via mpremote.
    
    Args:
        code: Validated Python code to flash
        target: Target architecture (esp32, rp2040, stm32)
        filename: Destination filename on device (default: driver.py)
        port: Serial port path (e.g., /dev/ttyUSB0, COM3)
        
    Returns:
        dict: Status with 'success' bool and 'message' string
        
    Raises:
        ValueError: If deployment fails
    """
    if not filename:
        filename = "driver.py"
        
    temp_file = f"/tmp/{filename}"
    
    try:
        with open(temp_file, "w") as f:
            f.write(code)
        
        cmd = ["mpremote"]
        if port:
            cmd.extend(["connect", port])
        cmd.extend(["cp", temp_file, f":{filename}"])
        
        logger.debug(f"Executing mpremote command for {target} on {port or 'default port'}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            error_msg = result.stderr.strip()[:200]  # Truncate to prevent log injection
            logger.error(f"mpremote flash failed for {target}: {error_msg}")
            raise ValueError(f"Failed to deploy driver to {target}. Check device connection and port.")
            
        logger.info(f"Successfully flashed {filename} to {target}")
        return {
            "success": True,
            "message": f"Successfully deployed {filename} to {target}"
        }
    except subprocess.TimeoutExpired:
        logger.error(f"mpremote timeout on {target}")
        raise ValueError(f"Device deployment timed out on {target}. Check device connectivity.")
    except Exception as e:
        logger.error(f"Deployment error on {target}: {type(e).__name__}")
        raise ValueError(f"Failed to deploy driver to {target}. Contact support if issue persists.")
    finally:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                logger.warning(f"Failed to clean up temp file {temp_file}: {e}")
