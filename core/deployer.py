import subprocess
import os

def flash_to_microcontroller(code: str, target: str, filename: str = None, port: str = None) -> str:
    # Determine default module filename based on target/peripheral if not provided
    if not filename:
        filename = "driver.py"
        
    temp_file = f"/tmp/{filename}"
    
    with open(temp_file, "w") as f:
        f.write(code)
        
    try:
        cmd = ["mpremote"]
        if port:
            cmd.extend(["connect", port])
        cmd.extend(["cp", temp_file, f":{filename}"])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            raise RuntimeError(f"mpremote flash error on {target}: {result.stderr.strip()}")
            
        return f"Successfully flashed {filename} to target [{target}]!"
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
