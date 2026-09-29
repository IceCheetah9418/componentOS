# Troubleshooting ComponentOS

## The API will not start

- Confirm the virtual environment is active.
- Run `pip install -r requirements.txt` again.
- Check that you are running `uvicorn main:app --reload` from the repository root.
- Visit `/docs` after startup to confirm the FastAPI service is reachable.

## Provider or authentication errors

- Check `LLM_PROVIDER`, `LLM_BASE_URL`, `LLM_MODEL`, and `PLANNER_MODEL` in `.env`.
- For cloud providers, verify the API key, account limits, and model name.
- For Ollama, confirm the service is running and the selected models are installed.
- Never paste API keys into issues or discussions.

## Generated code is rejected

The validator intentionally rejects unsupported or dangerous syntax. Inspect the validation output, simplify the request, and make the hardware requirements explicit. Do not disable safety checks just to force deployment.

## The board cannot be flashed

- Confirm the board is running MicroPython and is connected.
- Check the serial port (`/dev/ttyUSB0`, `/dev/ttyACM0`, or `COM3`).
- Close other serial monitors that may hold the port.
- Confirm `mpremote` is installed and available in the active environment.
- Check cable, permissions, power, pin assignments, and board-specific reset/boot instructions.
- Try `mpremote connect <port> fs ls` before using the synthesis endpoint.

## Hardware behaves incorrectly

Stop the deployment and disconnect power if the board or component becomes hot or behaves unexpectedly. Verify voltage levels, wiring, addresses, pull-ups, bus speed, and the peripheral datasheet. Model-generated drivers are suggestions and require human review before use.

## Still stuck?

Open a [discussion](https://github.com/IceCheetah9418/componentOS/discussions) for setup questions. For a reproducible defect, open an [issue](https://github.com/IceCheetah9418/componentOS/issues) using the bug template and include the board, peripheral, environment, request, and complete sanitized logs.
