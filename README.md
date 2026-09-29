# ComponentOS

> Autonomous MicroPython driver synthesis, validation, and deployment engine for embedded hardware (driver maker).

ComponentOS turns a natural language hardware request into a verified, production-ready MicroPython driver. A planner model maps out the implementation strategy, a coder model generates the firmware, an AST-based safety gate audits it, and an optional deployment pipeline flashes it directly to your connected microcontroller over serial connection ```(mpremote)```.

> **Project status:** Production sigmaness in progress. Generated firmware and deployment operations must be reviewed and tested on non-critical hardware before real-world deployment (basically test before actual big uses).

## Highlights

- **Hardware-aware synthesis** tailored for specific peripherals, bus protocols, pinouts, and target boards.
- **Provider flexibility** supporting OpenRouter, Ollama, and OpenAI-compatible endpoints.
- **Two-stage generation architecture** separating architectural planning from code generation.
- **AST-based safety validation** blocking forbidden imports, dynamic execution calls, and unsafe builtins.
- **API security & rate limiting** featuring header-based authentication (`x-api-key`) and per-client request throttling.
- **MicroPython deployment** using `mpremote` with built-in timeout safeguards and subprocess error sanitization.
- **Python API service** fully exposed through FastAPI and Uvicorn.

## How it works

```
Hardware request → Planner → Driver generator → AST safety validator → Optional mpremote deployment
```
Describe your peripheral, target board, and pin configuration.

The planner LLM produces a structured hardware implementation specification.

The coder LLM generates the clean MicroPython driver class.

ComponentOS passes the generated code through an AST safety audit.

If requested and authenticated, the validated driver is deployed directly to the target device.

Requirements
Python 3.10 or newer

A configured LLM provider: OpenRouter, Ollama, or an OpenAI-compatible API

mpremote and a connected MicroPython board for flashing

Target hardware such as an ESP32, RP2040/Pico, or STM32 microcontroller

Installation
```
git clone https://github.com/IceCheetah9418/componentOS.git
cd componentOS
python -m venv .venv
```
# macOS / Linux
```
source .venv/bin/activate
```
# Windows PowerShell
```
.venv\Scripts\Activate.ps1
```
Then:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Copy the environment template and configure your keys:
```
cp .env.example .env
```
Security Note: Never commit your .env file or API secrets to version control.

## Configuration Examples

OpenRouter
```
LLM_PROVIDER=openrouter
LLM_API_KEY=your_openrouter_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=your-coder-model
PLANNER_MODEL=your-planner-model
API_KEY=your-secure-api-key-here-change-in-production
```
Ollama (Local)
```
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=codellama
PLANNER_MODEL=llama3
API_KEY=your-secure-api-key-here-change-in-production
```
Run the API
```
uvicorn main:app --reload
```
Explore the interactive API documentation and test endpoints directly at http://127.0.0.1:8000/docs.

Example Request
All synthesis requests require your configured API key via the x-api-key header. Set flash to false when inspecting code or developing locally.

```
curl -X POST http://127.0.0.1:8000/synthesize \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: your-secure-api-key-here-change-in-production' \
  -d '{
    "peripheral": "MPU6050 6-axis accelerometer and gyroscope",
    "pinout": "SDA on pin 21, SCL on pin 22",
    "target": "esp32",
    "flash": false,
    "port": "/dev/ttyUSB0"
  }'
  ```
For Raspberry Pi Pico targets, use serial ports like /dev/ttyACM0 on Linux/macOS or COM3 on Windows.

Safety and Responsible Use
Generated code requires human verification. Review every synthesized driver, double-check pin assignments and operating voltages, and test using current-limited power supplies where possible. ComponentOS must not be used for medical, life-support, mission-critical, or hazardous automation systems without rigorous independent engineering validation.

The safety validator provides defense-in-depth, not an absolute sandbox. Review SECURITY.md for reporting guidelines and support/TROUBLESHOOTING.md for common hardware issues.
```
Repository Layout
Plaintext
main.py                 FastAPI service, rate limiting, and synthesis entry point
core/                   Planning, AST security validation, and mpremote deployment code
llm/                    Pluggable model provider integrations
node/                   Stateless device-side polling agent with sandboxed execution
tools/                  Development and hardware utility scripts
support/                User-facing troubleshooting guides and documentation
.github/                Issue templates, pull request checklists, and workflows
```
### Troubleshooting and Support

Check the troubleshooting guide first. When opening an issue or discussion, please include:

1. Your target board and MicroPython firmware version

2. The peripheral model and exact wiring/pinout configuration

3. Your host operating system and Python version

4. Active LLM provider settings (never include raw API keys)

5. Full error tracebacks or API JSON responses

6. A minimal reproducible request payload

Use GitHub Discussions for architecture questions and Issues for confirmed bugs and feature requests.

Contributing
Contributions are welcome! Please read CONTRIBUTING.md, adhere to our Code of Conduct, and use the provided PR templates.

License
ComponentOS is open-source software released under the MIT License.

Disclaimer: ComponentOS is provided as-is. Large language models can produce unexpected, flawed, or suboptimal output. You retain full responsibility for verifying generated code, hardware connections, credentials, and deployments.

NOTE: this is maintained by 1 guy, don't beg for updates or anything, he is trying to get more as soon as possible (me)
