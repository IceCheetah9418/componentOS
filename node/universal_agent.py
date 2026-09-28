import sys
import time
import json
import urllib.request
import signal
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Code execution timeout")

@contextmanager
def execution_timeout(seconds=10):
    """Context manager for code execution timeout."""
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

class UniversalAgent:
    def __init__(self, backend_url: str, node_id: str):
        self.backend_url = backend_url
        self.node_id = node_id
        self.MAX_EXECUTION_TIME = 10  # seconds
        self.MAX_OUTPUT_SIZE = 10000  # characters

    def execute_payload(self, code: str) -> dict:
        """Execute code with timeout and output size limits.
        
        Args:
            code: Python code to execute (pre-validated by backend)
            
        Returns:
            dict: Status and output/error message
        """
        try:
            local_vars = {}
            
            # Execute with timeout protection
            try:
                with execution_timeout(self.MAX_EXECUTION_TIME):
                    exec(code, {"__builtins__": {}}, local_vars)
            except TimeoutException:
                logger.error("Code execution exceeded timeout limit")
                return {"status": "error", "message": "Execution timeout: code ran too long"}
            
            # Limit output size to prevent memory exhaustion
            output_str = str(local_vars)
            if len(output_str) > self.MAX_OUTPUT_SIZE:
                output_str = output_str[:self.MAX_OUTPUT_SIZE] + "...[truncated]"
            
            return {"status": "success", "output": output_str}
            
        except Exception as e:
            error_msg = str(e)[:500]  # Truncate to prevent log injection
            logger.error(f"Execution error: {type(e).__name__}: {error_msg}")
            return {"status": "error", "message": f"Execution error: {type(e).__name__}"}

    def poll_loop(self, interval: int = 5):
        """Poll backend for code payloads and execute.
        
        Args:
            interval: Polling interval in seconds
        """
        logger.info(f"Starting poll loop for node {self.node_id} (interval={interval}s)")
        
        while True:
            try:
                req = urllib.request.Request(
                    f"{self.backend_url}/node/poll/{self.node_id}",
                    headers={"User-Agent": "ComponentOS-Agent"}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    if "code" in data:
                        logger.info(f"Received code payload from backend")
                        result = self.execute_payload(data["code"])
                        
                        report_req = urllib.request.Request(
                            f"{self.backend_url}/node/report",
                            data=json.dumps({"node_id": self.node_id, "result": result}).encode(),
                            headers={"Content-Type": "application/json"},
                            method="POST"
                        )
                        try:
                            urllib.request.urlopen(report_req, timeout=5)
                            logger.debug("Result reported to backend")
                        except Exception as e:
                            logger.error(f"Failed to report result: {e}")
                            
            except urllib.error.URLError as e:
                logger.debug(f"Backend unreachable: {e}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from backend: {e}")
            except Exception as e:
                logger.error(f"Unexpected error in poll loop: {type(e).__name__}: {str(e)[:200]}")
                
            time.sleep(interval)
