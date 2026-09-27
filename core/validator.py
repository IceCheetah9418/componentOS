import ast

class SecurityValidator(ast.NodeVisitor):
    def __init__(self):
        self.allowed_modules = {
            "machine", "time", "utime", "network", 
            "esp32", "math", "dht", "struct", "ustruct", "micropython"
        }
        self.forbidden_builtins = {"eval", "exec", "compile", "__import__", "open"}
        self.errors = []

    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module not in self.allowed_modules:
                self.errors.append(f"Forbidden module import detected: {base_module}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            base_module = node.module.split(".")[0]
            if base_module not in self.allowed_modules:
                self.errors.append(f"Forbidden module import detected: {base_module}")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.forbidden_builtins:
                self.errors.append(f"Forbidden function call detected: {node.func.id}()")
        self.generic_visit(node)

def validate_code(code_string: str) -> tuple[bool, list[str]]:
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return False, [f"Python Syntax Error: {e}"]
    
    validator = SecurityValidator()
    validator.visit(tree)
    
    if validator.errors:
        return False, validator.errors
    return True, []
