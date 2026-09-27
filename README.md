# ComponentOS 🔌🤖

Super ULTRA dual-llm setup that auto-synthesizes, validates, and flashes custom Micro-Python drivers straight to your microcontrollers. Planner + Coder figures out the specs and writes the code, Iron Gate AST checker keeps it safe, and `mpremote` pushes it right to the metal (optional and its for flashing). No more writing tedious boilerplate sensor code from scratch, BRUH.

---

## 🧐 What is ComponentOS?

ComponentOS is an autonomous microcode synthesis engine designed to bridge the gap between human peripheral intent and physical embedded hardware. Instead of spending hours hunting down half-baked GitHub drivers or reading 80-page datasheets for I2C register maps, ComponentOS generates hardware-accurate, security-audited MicroPython drivers on demand and pushes them directly onto your microcontrollers.

---

## 🛠️ How It Works (The Engine Pipeline)

ComponentOS uses a decoupled pipeline to make sure synthesized code isn't just valid Python, but actual functional firmware that won't crash your microcontroller or hang your bus:

1. **Architectural Planning Phase (Planner LLM):**
   * Uses `nvidia/nemotron-3-ultra-550b-a55b` to act as an embedded hardware architect.
   * Scans datasheets and pinouts to output precise technical specifications: I2C/SPI clock speeds, rise-time constraints, register initialization sequences, power-on delays, and burst-read byte offsets.

2. **Firmware Synthesis Phase (Coder LLM):**
   * Uses `cohere/north-mini-code` to take the spec from the Planner and convert it into a lean, production-ready MicroPython class.
   * Generates low-level write/read register helpers, unit conversions (like converting raw LSB to $g$ force or °/s), and automatic hardware bias calibration routines.

3. **Iron Gate Security Audit (AST Validator):**
   * Parses the generated code using Python's Abstract Syntax Tree (`ast`).
   * Enforces strict execution safety by blocking dangerous built-ins (`eval`, `exec`, `open`, `__import__`) and ensuring only approved hardware modules (`machine`, `time`, `math`, `struct`) are imported.

4. **Universal Metal Deployment (`mpremote`):**
   * Integrates MicroPython's native CLI tool (`mpremote`) directly into the backend.
   * Stages the validated driver and flashes it over serial/USB directly onto the board's filesystem (`:driver.py`) across any target architecture (ESP32, Raspberry Pi Pico RP2040, STM32, ESP8266).

---

## ⚡ Quick Setup

Clone the repository and set up your Python virtual environment:

```
git clone [https://github.com/IceCheetah9418/componentOS.git](https://github.com/IceCheetah9418/componentOS.git) && cd componentOS
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
Drop a .env file in the root directory:

Code snippet
```
LLM_PROVIDER=openrouter
LLM_API_KEY=your_key_here
LLM_BASE_URL=[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)
LLM_MODEL=cohere/north-mini-code:free
PLANNER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```
Fire up the backend server:

```
uvicorn main:app --reload
```
🧪 Test It Out (Random Examples)
You can send a POST request to http://127.0.0.1:8000/synthesize using curl or any API client.

Example 1: MPU6050 Accelerometer on ESP32
```
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
```
📌 Note
Note: This is a solo project built and maintained by one person! New features, UI dashboards, and updates are being actively cooked up, but they might take a little while. Appreciate the patience, BRUH!
