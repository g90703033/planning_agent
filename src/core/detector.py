import platform
import shutil
import os

class EnvironmentDetector:
    def detect_os(self) -> str:
        return platform.system()

    def detect_shell(self) -> str:
        # Simplified shell detection
        if platform.system() == "Windows":
            return "powershell"
        return "bash"

    def scan_tools(self) -> dict:
        tools = ["python", "git", "docker", "node", "npm"]
        found_tools = {}
        for tool in tools:
            path = shutil.which(tool)
            if path:
                found_tools[tool] = path
        return found_tools
