# ComponentOS 🔌🤖

Super ULTRA dual-llm setup that auto-synthesizes, validates, and flashes custom Micro-Python drivers straight to your microcontrollers. Planner + Coder figures out the specs and writes the code, Iron Gate AST checker keeps it safe, and `mpremote` pushes it right to the metal (optional and its for flashing). No more writing tedious boilerplate sensor code from scratch, BRUH.

## Quick Setup

```
git clone [https://github.com/IceCheetah9418/componentOS.git](https://github.com/IceCheetah9418/componentOS.git) && cd componentOS
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
Drop a .env file in the root:
```
Code snippet
LLM_PROVIDER=openrouter
LLM_API_KEY=your_key_here
LLM_BASE_URL=[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)
LLM_MODEL=cohere/north-mini-code:free
PLANNER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```
Fire up the backend:

```
uvicorn main:app --reload
Test It Out (Random Examples)
Example 1: MPU6050 Accelerometer on ESP32
Bash
curl -X 'POST' '[http://127.0.0.1:8000/synthesize](http://127.0.0.1:8000/synthesize)' \
  -H 'Content-Type: application/json' \
  -d '{
    "peripheral": "MPU6050 6-axis accelerometer and gyroscope",
    "pinout": "SDA on pin 21, SCL on pin 22",
    "target": "esp32",
    "flash": true,
    "port": "/dev/ttyUSB0"
  }'
```
Example 2: DHT22 Sensor on PI Pico
```
curl -X 'POST' '[http://127.0.0.1:8000/synthesize](http://127.0.0.1:8000/synthesize)' \
  -H 'Content-Type: application/json' \
  -d '{
    "peripheral": "DHT22 temperature and humidity sensor",
    "pinout": "Data on GPIO 15",
    "target": "rp2040",
    "flash": true,
    "port": "/dev/ttyACM0"
  }'
