from llm.providers import get_llm_provider
from core.validator import validate_code

class DriverSynthesisEngine:
    def __init__(self):
        self.planner = get_llm_provider(role="planner")
        self.coder = get_llm_provider(role="coder")

    def synthesize(self, peripheral: str, pinout: str, target: str = "esp32") -> dict:
        planning_prompt = f"""
        Analyze the following hardware peripheral and pinout requirement for a MicroPython target ({target}):
        Peripheral: {peripheral}
        Pinout/Pins: {pinout}
        Target Microcontroller: {target}
        
        Provide a concise technical specification detailing the protocol, timing constraints, 
        register initialization sequence, and target-specific hardware considerations.
        """
        plan = self.planner.generate(
            prompt=planning_prompt, 
            system_prompt=f"You are an expert embedded systems architect specializing in {target} microcode."
        )

        coding_prompt = f"""
        Using the architectural plan, write a clean, production-ready MicroPython class for target [{target}].
        Return ONLY valid Python code without markdown text blocks if possible.
        
        Architectural Plan:
        {plan}
        """
        raw_code = self.coder.generate(
            prompt=coding_prompt, 
            system_prompt="You are a strict MicroPython firmware engineer writing clean, robust driver classes."
        )

        clean_code = raw_code.replace("```python", "").replace("```", "").strip()

        is_valid, error_msg = validate_code(clean_code)
        if not is_valid:
            raise ValueError(f"Iron Gate Validation Failed: {error_msg}")

        return {
            "target": target,
            "plan": plan,
            "code": clean_code
        }
