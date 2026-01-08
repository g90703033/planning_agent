from typing import List, Dict, Any
from src.utils.llm import LLM
from src.core.memory import Memory

class Planner:
    def __init__(self, llm: LLM, memory: Memory):
        self.llm = llm
        self.memory = memory

    def create_plan(self, task: str, context: Dict[str, Any], feedback: str = None) -> List[Dict[str, Any]]:
        # Construct a prompt with context
        system_instruction = (
            "You are an expert coding agent. \n"
            "First, analyze the task and explain your reasoning/design in a few sentences.\n"
            "Then, return your plan as a JSON list of steps wrapped in ```json ... ``` code blocks.\n\n"
            "Allowed step types:\n"
            "1. {\"type\": \"command\", \"command\": \"...\", \"background\": true/false} - Run a shell command. Set background=true for servers.\n"
            "2. {\"type\": \"write_file\", \"filename\": \"...\", \"content\": \"...\"} - Write a file.\n"
            "3. {\"type\": \"read_file\", \"filename\": \"...\"} - Read a file.\n"
            "4. {\"type\": \"search_files\", \"pattern\": \"...\", \"path\": \"...\"} - Search for a pattern in files (grep-like).\n"
            "5. {\"type\": \"verify\", \"command\": \"...\"} - Run a verification command to check if the task was completed successfully.\n"
            "6. {\"type\": \"ask_user\", \"question\": \"...\"} - Ask the user for missing information. The response will be available in the next planning cycle.\n"
            "Note: You are working in a clean, isolated project directory. You do not need to create a folder.\n"
            "IMPORTANT: You MUST include a final 'verify' step to check if your task was completed successfully."
        )
        
        prompt = f"Task: {task}\n\nEnvironment: {context}\n\n"
        if "files" in context:
            prompt += f"Files: {context['files']}\n\n"
            
        if feedback:
            prompt += f"PREVIOUS ATTEMPT FAILED. Feedback: {feedback}\n"
            prompt += "Please provide a corrected plan to fix the error.\n\n"
            
        prompt += "Plan:"
        
        response = self.llm.generate(prompt, system_instruction)
        
        try:
            # Attempt to parse JSON response
            import json
            import re
            
            # Find JSON block using regex
            match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
            if match:
                json_str = match.group(1)
                return json.loads(json_str)
            
            # Fallback: try to find list brackets if no code blocks
            match = re.search(r"\[.*\]", response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
                
            # If strictly JSON
            return json.loads(response)
        except (json.JSONDecodeError, AttributeError):
            print(f"Failed to parse plan: {response}")
            with open("debug_response.txt", "w", encoding="utf-8") as f:
                f.write(response)
            # Fallback to a simple command if parsing fails
            return [{"type": "command", "command": f"echo 'Could not parse plan for: {task}'"}]

