import sys
import argparse
from dotenv import load_dotenv
from src.core.coordinator import Coordinator

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Open-World LLM Agent")
    parser.add_argument("task", nargs="?", help="The task to perform")
    args = parser.parse_args()

    if not args.task:
        print("Please provide a task.")
        sys.exit(1)

    coordinator = Coordinator()
    coordinator.run(args.task)

if __name__ == "__main__":
    main()
