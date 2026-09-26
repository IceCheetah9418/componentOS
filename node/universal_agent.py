import sys
import time
import json
import urllib.request

class UniversalAgent:
    def __init__(self, backend_url: str, node_id: str):
        self.backend_url = backend_url
        self.node_id = node_id

    def execute_payload(self, code: str):
        try:
            local_vars = {}
            exec(code, {}, local_vars)
            return {"status": "success", "output": str(local_vars)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def poll_loop(self, interval: int = 5):
        while True:
            try:
                req = urllib.request.Request(
                    f"{self.backend_url}/node/poll/{self.node_id}",
                    headers={"User-Agent": "ComponentOS-Agent"}
                )
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())
                    if "code" in data:
                        result = self.execute_payload(data["code"])
                        report_req = urllib.request.Request(
                            f"{self.backend_url}/node/report",
                            data=json.dumps({"node_id": self.node_id, "result": result}).encode(),
                            headers={"Content-Type": "application/json"},
                            method="POST"
                        )
                        urllib.request.urlopen(report_req)
            except Exception:
                pass
            time.sleep(interval)
