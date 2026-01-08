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
        elif step_type == "search_files":
            return self._search_files(step, cwd)
        elif step_type == "verify":
            return self._verify_step(step, cwd)
        elif step_type == "ask_user":
            return self._execute_ask_user(step, cwd)
            
        return {"status": "skipped", "reason": f"unknown step type: {step_type}"}

    def _execute_ask_user(self, step: Dict[str, Any], cwd: str) -> Dict[str, Any]:
        question = step["question"]
        print(f"\n❓ AGENT ASKS: {question}")
        try:
            user_response = input("   Your Answer: ").strip()
            return {
                "status": "success",
                "output": user_response
            }
        except EOFError:
             return {"status": "failure", "error": "User input stream closed."}

    def _verify_step(self, step: Dict[str, Any], cwd: str) -> Dict[str, Any]:
        print(f"--- VERIFICATION STEP: {step['command']} ---")
        # Reuse command execution logic
        return self._execute_command(step, cwd)
            
        return {"status": "skipped", "reason": f"unknown step type: {step_type}"}

    def _execute_command(self, step: Dict[str, Any], cwd: str) -> Dict[str, Any]:
        command = step["command"]
        is_background = step.get("background", False)
        
        print(f"Executing in {cwd}: {command} (Background: {is_background})")
        try:
            if is_background:
                # Start process and return immediately
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return {
                    "status": "success",
                    "message": f"Command started in background with PID {proc.pid}",
                    "pid": proc.pid
                }
            else:
                # Run synchronously
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=cwd,
                    timeout=60 # Default timeout
                )
                return {
                    "status": "success" if result.returncode == 0 else "failure",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
        except subprocess.TimeoutExpired:
            return {
                "status": "failure",
                "error": "Command timed out after 60 seconds."
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

    def _search_files(self, step: Dict[str, Any], cwd: str) -> Dict[str, Any]:
        import os
        import subprocess
        
        pattern = step["pattern"]
        search_path = step.get("path", ".")
        
        # Use grep (or findstr on windows if grep not available, but git bash usually has grep)
        # For cross-platform python-only search:
        print(f"Searching for '{pattern}' in {search_path}")
        matches = []
        try:
            for root, _, files in os.walk(os.path.join(cwd, search_path)):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", errors='ignore') as f:
                            for i, line in enumerate(f, 1):
                                if pattern in line:
                                    rel_path = os.path.relpath(filepath, cwd)
                                    matches.append(f"{rel_path}:{i}: {line.strip()}")
                    except:
                        pass # Skip unreadable files
            
            return {
                "status": "success", 
                "matches": matches[:50], # Limit results
                "count": len(matches)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

