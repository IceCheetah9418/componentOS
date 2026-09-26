
import os
from llm.providers import get_llm_provider
from core.validator import validate_code

class ComponentOSEngine:
    def __init__(self):
        self.llm = get_llm_provider()

    def synthesize_driver(self, peripheral_spec: str, pinout: str) -> str:
        system_prompt = (
            "You are an expert MicroPython/Python hardware driver synthesis engine. "
            "Generate raw, executable MicroPython code for the requested peripheral. "
            "Only output valid Python code without markdown code blocks or explanations."
        )
        prompt = f"Peripheral: {peripheral_spec}\nPinout mapping: {pinout}"
        
        generated_code = self.llm.generate(prompt, system_prompt)
        
        if generated_code.startswith("```python"):
            generated_code = generated_code[9:]
        if generated_code.startswith("```"):
            generated_code = generated_code[3:]
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
        generated_code = generated_code.strip()

        is_valid, errors = validate_code(generated_code)
        if not is_valid:
            raise ValueError(f"Generated code failed security validation: {errors}")

        return generated_code
