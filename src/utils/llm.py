import os
import json
import urllib.request
import urllib.error

class LLM:
    def __init__(self, provider="gemini"):
        self.provider = provider
        self.api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if self.api_key:
            self.api_key = self.api_key.strip()
        
    def generate(self, prompt: str, system_instruction: str = None) -> str:
        if not self.api_key:
            print("WARNING: No API key found. Using mock response.")
            return self._mock_generate(prompt)
            
        if self.provider == "gemini":
            return self._call_gemini(prompt, system_instruction)
        
        print(f"Provider {self.provider} not implemented. Using mock.")
        return self._mock_generate(prompt)

    def _call_gemini(self, prompt: str, system_instruction: str = None) -> str:
        # Using gemini-flash-latest
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.api_key}"
        
        # Construct payload
        contents = [{"parts": [{"text": prompt}]}]
        if system_instruction:
             # Gemini API supports system instructions differently, but for simplicity we'll prepend it
             contents[0]["parts"][0]["text"] = f"System: {system_instruction}\n\nUser: {prompt}"

        data = {
            "contents": contents
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                # Extract text from response
                return result['candidates'][0]['content']['parts'][0]['text']
        except urllib.error.HTTPError as e:
            print(f"Error calling Gemini API: {e}")
            print(f"Response body: {e.read().decode('utf-8')}")
            return self._mock_generate(prompt)
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._mock_generate(prompt)

    def _mock_generate(self, prompt: str) -> str:
        # Simple heuristic mock for testing coding tasks
        if "fibonacci" in prompt.lower():
            return json.dumps([
                {"type": "write_file", "filename": "fib.py", "content": "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)\n\nprint(fib(10))"}
            ])
        if "verify" in prompt.lower():
            return json.dumps([
                {"type": "write_file", "filename": "verification_test.txt", "content": "PASSED"},
                {"type": "verify", "command": "type verification_test.txt"}
            ])
        if "ask" in prompt.lower():
            return json.dumps([
                {"type": "ask_user", "question": "What is your favorite color?"},
                {"type": "command", "command": "echo 'User said their favorite color is...'"} 
            ])
        return "Mock LLM Response"

