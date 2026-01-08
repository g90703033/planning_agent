# Open-World LLM Agent

An agent that can:
1.  Accept user tasks.
2.  Detect environment (OS, tools).
# Open-World LLM Agent

An agent that can:
1.  Accept user tasks.
2.  Detect environment (OS, tools).
3.  Generate plans using LLM + procedural memory.
4.  Execute safely.
5.  **Verify results.**
6.  Observe and learn.

## Usage

### Interactive Mode (Recommended)
Run the agent without arguments to enter the interactive shell. This allows you to maintain context across multiple commands.
```bash
python -m src.main
```
Inside the shell:
- Enter your task (e.g., "Create a snake game")
- Type `new` to switch to a fresh project workspace.
- Type `exit` to quit.

### Single Task Mode
Run a single task and exit:
```bash
python -m src.main "Your task here"
```

## Features
- **Project Isolation**: Each new task gets its own folder in `projects/`.
- **Persistence**: In interactive mode, the agent remembers your current project.
- **Self-Correction**: Automatically retries and fixes code if execution fails.
- **Verification Phase**: Explicitly verifies that tasks are completed successfully using the **Plan → Execute → Verify** workflow.
- **Environment Awareness**: Detects your OS and installed tools.
