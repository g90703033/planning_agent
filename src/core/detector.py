import platform
import shutil
import os

class EnvironmentDetector:
    def detect_os(self) -> str:
        return platform.system()

    def detect_shell(self) -> str:
        # Check for SHELL environment variable first
        shell_env = os.environ.get('SHELL')
        if shell_env:
            return os.path.basename(shell_env)
            
        if platform.system() == "Windows":
            return "powershell"
        return "bash"

    def scan_tools(self) -> dict:
        # Expanded list of common development tools
        tools = [
            "python", "git", "docker", "node", "npm",
            "gcc", "g++", "make", "cmake",
            "go", "rustc", "cargo",
            "java", "javac", "mvn", "gradle"
        ]
        found_tools = {}
        for tool in tools:
            path = shutil.which(tool)
            if path:
                found_tools[tool] = path
        return found_tools
