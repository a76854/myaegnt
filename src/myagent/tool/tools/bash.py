import os
import subprocess

from .basetool import BaseTool


class BashTool(BaseTool):
    name = "bash"
    description = "Execute bash commands on the local machine."
    schema = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The bash command to be executed."
            }
        },
        "required": ["command"]
    }
    dangerous_commands = tuple(["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"])

    def run(self, command: str) -> str:
        if any(d in command for d in self.dangerous_commands):
            return "Error: Dangerous command blocked"
        try:
            r = subprocess.run(command, shell=True, cwd=os.getcwd(),
                               capture_output=True, text=True, timeout=120)
            out = (r.stdout + r.stderr).strip()
            return out[:50000] if out else "(no output)"
        except subprocess.TimeoutExpired:
            return "Error: Timeout (120s)"
        except (FileNotFoundError, OSError) as e:
            return f"Error: {e}"
