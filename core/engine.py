from llm.providers import get_llm_provider
from core.validator import validate_code

class DriverSynthesisEngine:
    def __init__(self):
        self.planner = get_llm_provider(role="planner")
        self.coder = get_llm_provider(role="coder")

    def synthesize(self, peripheral: str, pinout: str) -> dict:
        # Step 1: Planner Agent designs the hardware approach & pin mapping strategy
        planning_prompt = f"""
        Analyze the following hardware peripheral and pinout requirement for an ESP32 microcode target:
        Peripheral: {peripheral}
        Pinout: {pinout}
        
        Provide a concise technical specification detailing the protocol (e.g., I2C, SPI, GPIO, One-Wire), 
        timing constraints, initialization sequence, and safety considerations.
        """
        plan = self.planner.generate(
            prompt=planning_prompt, 
            system_prompt="You are an embedded systems hardware architect."
        )

        # Step 2: Coder Agent writes the strict MicroPython driver based on the plan
        coding_prompt = f"""
        Using the following architectural plan, write a clean, production-ready MicroPython class for the ESP32.
        Return ONLY valid Python code without markdown text blocks if possible, or standard clean code.
        
        Architectural Plan:
        {plan}
        """
        raw_code = self.coder.generate(
            prompt=coding_prompt, 
            system_prompt="You are a strict MicroPython firmware engineer writing clean, robust driver classes."
        )

        # Clean markdown code blocks if the LLM wrapped them
        clean_code = raw_code.replace("```python", "").replace("```", "").strip()

        # Step 3: Run through the Iron Gate AST Validator for safety
        is_valid, error_msg = validate_code(clean_code)
        if not is_valid:
            raise ValueError(f"Iron Gate Validation Failed: {error_msg}")

        return {
            "plan": plan,
            "code": clean_code
        }
