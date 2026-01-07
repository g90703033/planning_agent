import subprocess
from typing import Dict, Any

class Executor:
    def execute_step(self, step: Dict[str, Any], cwd: str = ".") -> Dict[str, Any]:
        step_type = step.get("type")
        
        if step_type == "command":
            return self._execute_command(step, cwd)
        elif step_type == "write_file":
            return self._write_file(step, cwd)
        elif step_type == "read_file":
            return self._read_file(step, cwd)
            
        return {"status": "skipped", "reason": f"unknown step type: {step_type}"}

    def _execute_command(self, step: Dict[str, Any], cwd: str) -> Dict[str, Any]:
        command = step["command"]
        print(f"Executing in {cwd}: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=60
            )
            return {
                "status": "success" if result.returncode == 0 else "failure",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _write_file(self, step: Dict[str, Any], cwd: str) -> Dict[str, Any]:
        import os
        filename = step["filename"]
        content = step["content"]
        path = os.path.join(cwd, filename)
        print(f"Writing file: {path}")
        try:
            with open(path, "w") as f:
                f.write(content)
            return {"status": "success", "message": f"File {filename} written."}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _read_file(self, step: Dict[str, Any], cwd: str) -> Dict[str, Any]:
        import os
        filename = step["filename"]
        path = os.path.join(cwd, filename)
        print(f"Reading file: {path}")
        try:
            with open(path, "r") as f:
                content = f.read()
            return {"status": "success", "content": content}
        except Exception as e:
            return {"status": "error", "error": str(e)}

