import ast
from pathlib import Path


class NegocioValidationService:
    def validate_python_syntax(self, file_path: Path | str) -> dict:
        path = Path(file_path)
        try:
            code = path.read_text(encoding="utf-8")
            ast.parse(code)
            return {"valid": True, "errors": []}
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [{
                    "line": e.lineno,
                    "offset": e.offset,
                    "message": e.msg,
                    "text": e.text,
                }],
            }

    def validate_prompt_structure(self, prompt: str, template_name: str = "default") -> dict:
        required_sections = ["context", "code", "tests"]
        prompt_lower = prompt.lower()
        missing = [s for s in required_sections if s not in prompt_lower]
        if missing:
            return {
                "valid": False,
                "errors": [f"Missing required section(s): {', '.join(missing)}"],
            }
        return {"valid": True, "errors": []}
