from src.core.detector import EnvironmentDetector
from src.core.memory import Memory
from src.core.planner import Planner
from src.core.executor import Executor
from src.core.reflector import Reflector
from src.utils.llm import LLM

class Coordinator:
    def __init__(self):
        self.detector = EnvironmentDetector()
        self.memory = Memory()
        self.llm = LLM()
        self.planner = Planner(self.llm, self.memory)
        self.executor = Executor()
        self.reflector = Reflector(self.memory)

    def run(self, task: str):
        print(f"Starting task: {task}")
        
        # 0. Create Workspace
        workspace_path = self._create_workspace(task)
        print(f"Workspace: {workspace_path}")
        
        # 1. Detect Environment
        env_info = {
            "os": self.detector.detect_os(),
            "shell": self.detector.detect_shell(),
            "tools": self.detector.scan_tools(),
            "files": self._list_files(workspace_path),
            "cwd": workspace_path
        }
        print(f"Environment: {env_info}")

        # 2. Plan
        plan = self.planner.create_plan(task, env_info)
        print(f"Plan: {plan}")

        # 3. Execute
        execution_trace = {
            "task": task,
            "plan": plan,
            "steps": [],
            "workspace": workspace_path
        }
        
        success = True
        for step in plan:
            result = self.executor.execute_step(step, cwd=workspace_path)
            execution_trace["steps"].append({
                "step": step,
                "result": result
            })
            if result["status"] != "success":
                success = False
                print(f"Step failed: {result}")
                break
        
        execution_trace["status"] = "success" if success else "failure"

        # 4. Reflect
        self.reflector.reflect(execution_trace)
        self.memory.add_trace(execution_trace)
        
        print("Task completed.")

    def _create_workspace(self, task: str) -> str:
        import datetime
        import re
        import os
        
        # Create projects directory
        projects_dir = "projects"
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)
            
        # Generate slug
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = re.sub(r'[^a-zA-Z0-9]', '_', task[:30]).lower()
        folder_name = f"{timestamp}_{slug}"
        workspace_path = os.path.join(projects_dir, folder_name)
        
        if not os.path.exists(workspace_path):
            os.makedirs(workspace_path)
            
        return workspace_path

    def _list_files(self, directory):
        import os
        files = []
        if not os.path.exists(directory):
            return []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if ".git" not in root:
                    files.append(os.path.join(root, filename))
        return files[:20] # Limit to 20 files for context

