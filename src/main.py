import sys
import argparse
from dotenv import load_dotenv
from src.core.coordinator import Coordinator

import sys
import argparse
from dotenv import load_dotenv
from src.core.coordinator import Coordinator

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Open-World LLM Agent")
    parser.add_argument("task", nargs="?", help="The task to perform")
    args = parser.parse_args()

    coordinator = Coordinator()

    # Interactive Mode
    
    current_workspace = None
    
    # If a task is provided as a command-line argument, run it once
    if args.task:
        coordinator.run(args.task)
        return

    # Otherwise, enter interactive loop
    print("--- Agent Interactive Mode ---")
    print("Commands:")
    print("  new  - Start a new project")
    print("  exit - Exit the agent")
    print("------------------------------")
    
    while True:
        prompt = f"(Current: {current_workspace}) " if current_workspace else "(New Project) "
        try:
            task = input(f"{prompt}Enter task: ").strip()
        except EOFError:
            break
            
        if not task:
            continue
            
        if task.lower() == "exit":
            break
        
        if task.lower() == "new":
            current_workspace = None
            print("Switched to new project context.")
            continue
            
        try:
            current_workspace = coordinator.run(task, workspace_path=current_workspace)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
