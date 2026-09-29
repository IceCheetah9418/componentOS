# ComponentOS

> Dynamic MicroPython driver synthesis and deployment for embedded hardware.

ComponentOS turns a hardware request into a validated MicroPython driver. A planner model creates an implementation plan, a coder model generates the driver, an AST-based safety gate checks it, and the optional deployment step sends it to a connected board.

> **Project status:** Early-stage and experimental. Generated firmware must be reviewed and tested on non-critical hardware before production use.

## Highlights

- **Hardware-aware synthesis** for peripherals, buses, pins, and target boards.
- **Provider flexibility** through OpenRouter, Ollama, and OpenAI-compatible endpoints.
- **Two-stage generation** separating hardware planning from code generation.
- **Safety validation** before generated code is accepted for deployment.
- **MicroPython deployment** through `mpremote` over USB or serial.
- **Python API service** exposed through FastAPI/Uvicorn.

## How it works

```text
Hardware request → Planner → Driver generator → AST safety validator → Optional mpremote deployment
```

1. Describe the peripheral, board, pins, and desired behavior.
2. The planner produces a hardware implementation specification.
3. The coder generates a MicroPython driver.
4. ComponentOS validates the generated source against its safety rules.
5. If requested, the validated driver is copied to the board.

## Requirements

- Python 3.10 or newer
- A supported LLM provider: OpenRouter, Ollama, or another OpenAI-compatible API
- `mpremote` and a connected MicroPython board for flashing
- A board such as ESP32, RP2040/Pico, or another compatible MicroPython target

## Installation

```bash
git clone https://github.com/IceCheetah9418/componentOS.git
cd componentOS
python -m venv .venv

# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy the example configuration and edit it:

```bash
cp .env.example .env
```

Never commit `.env` or API keys. For local development, Ollama can keep prompts and generated code on your own machine.

### OpenRouter

```dotenv
LLM_PROVIDER=openrouter
LLM_API_KEY=your_openrouter_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=your-coder-model
PLANNER_MODEL=your-planner-model
```

### Ollama

```dotenv
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=codellama
PLANNER_MODEL=llama3
```

## Run the API

```bash
uvicorn main:app --reload
```

Open the interactive API documentation at <http://127.0.0.1:8000/docs>.

## Example request

This generates a driver for an MPU6050 connected to an ESP32. Set `flash` to `false` while developing or when you only want to inspect the result.

```bash
curl -X POST http://127.0.0.1:8000/synthesize \
  -H 'Content-Type: application/json' \
  -d '{
    "peripheral": "MPU6050 6-axis accelerometer and gyroscope",
    "pinout": "SDA on pin 21, SCL on pin 22",
    "target": "esp32",
    "flash": false,
    "port": "/dev/ttyUSB0"
  }'
```

For a Pico, use a port such as `/dev/ttyACM0` on Linux/macOS or `COM3` on Windows.

## Safety and responsible use

Generated code is not automatically safe simply because it passes validation. Review every driver, verify pin assignments and voltage levels, and test with current-limited power where possible. Do not use ComponentOS for medical, life-support, safety-critical, or hazardous-control systems without independent engineering review.

The validator is a defense-in-depth feature, not a sandbox. See [SECURITY.md](SECURITY.md) for reporting vulnerabilities and [support/TROUBLESHOOTING.md](support/TROUBLESHOOTING.md) for common problems.

## Repository layout

```text
main.py                 FastAPI service and synthesis entry point
core/                   Planning, validation, and orchestration code
llm/                    Model/provider integrations
node/                   Device/node-side code
tools/                  Development and deployment utilities
support/                User-facing troubleshooting documentation
.github/                Issue forms, pull request guidance, and workflows
```

## Troubleshooting and support

Start with the [troubleshooting guide](support/TROUBLESHOOTING.md). When opening an issue, include:

- board and MicroPython version;
- peripheral model and wiring/pinout;
- operating system and Python version;
- provider/model configuration (never include API keys);
- the complete traceback or API response;
- a minimal request that reproduces the problem.

Use [GitHub Discussions](https://github.com/IceCheetah9418/componentOS/discussions) for questions and ideas, and [Issues](https://github.com/IceCheetah9418/componentOS/issues) for reproducible bugs and actionable feature requests.

## Contributing

Pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md), follow the [Code of Conduct](CODE_OF_CONDUCT.md), and use the provided issue and pull request templates.

## License

ComponentOS is released under the [MIT License](LICENSE).

## Disclaimer

ComponentOS is provided as-is. Model output can be incorrect, incomplete, or unsafe. You are responsible for validating generated code, hardware connections, credentials, and deployments.
