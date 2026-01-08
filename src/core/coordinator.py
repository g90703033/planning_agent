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

    def run(self, task: str, workspace_path: str = None) -> str:
        print(f"Starting task: {task}")
        
        # 0. Create or Reuse Workspace
        if not workspace_path:
            workspace_path = self._create_workspace(task)
        print(f"Workspace: {workspace_path}")
        
        # 1. Detect Environment
        env_info = {
            "os": self.detector.detect_os(),
            "shell": self.detector.detect_shell(),
            "tools": self.detector.scan_tools(),
            "files": self._generate_tree_view(workspace_path),
            "cwd": workspace_path
        }
        print(f"Environment: {env_info}")

        # 2. Plan & Execute Loop
        max_retries = 50
        attempt = 0
        feedback = None
        
        while attempt < max_retries:
            attempt += 1
            print(f"--- Attempt {attempt}/{max_retries} ---")
            
            # Plan
            plan = self.planner.create_plan(task, env_info, feedback)
            print(f"Plan: {plan}")

            # Execute
            execution_trace = {
                "task": task,
                "plan": plan,
                "steps": [],
                "workspace": workspace_path
            }
            
            success = True
            error_message = ""
            
            for step in plan:
                result = self.executor.execute_step(step, cwd=workspace_path)
                execution_trace["steps"].append({
                    "step": step,
                    "result": result
                })
                
                if result["status"] != "success":
                    success = False
                    # Capture error for feedback
                    error_message = result.get("stderr") or result.get("error") or result.get("reason") or "Unknown error"
                    
                    if step.get("type") == "verify":
                        print(f"❌ VERIFICATION FAILED: {error_message}")
                    else:
                        print(f"Step failed: {result}")
                    break
            
            execution_trace["status"] = "success" if success else "failure"
            self.memory.add_trace(execution_trace)
            
            if success:
                print("Task completed successfully.")
                break
            else:
                feedback = f"Execution failed at step: {step}. Error: {error_message}"
                print(f"Attempt failed. Retrying with feedback: {feedback}")

        # 4. Reflect
        self.reflector.reflect(execution_trace)
        
        return workspace_path

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

    def _generate_tree_view(self, directory: str, prefix: str = "") -> str:
        import os
        if not os.path.exists(directory):
            return ""
            
        tree_str = ""
        items = sorted(os.listdir(directory))
        items = [i for i in items if i not in [".git", "__pycache__", ".venv", ".env"]]
        
        for i, item in enumerate(items):
            path = os.path.join(directory, item)
            is_last = (i == len(items) - 1)
            
            connector = "└── " if is_last else "├── "
            tree_str += f"{prefix}{connector}{item}\n"
            
            if os.path.isdir(path):
                extension = "    " if is_last else "│   "
                tree_str += self._generate_tree_view(path, prefix + extension)
                
        return tree_str

