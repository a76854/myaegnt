from .basetool import BaseTool, safe_path


class ReadFile(BaseTool):
    name = "readFile"
    description = "Reads the content of a specified file."
    schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to be read."
            },
            "limit": {
                "type": "integer",
                "description": "The maximum number of characters to read from the file."
            }
        },
        "required": ["file_path", "limit"]
    }

    def run(self, file_path: str, limit: int) -> str:
        try:
            abs_path = safe_path(file_path)
            with open(abs_path) as file:
                content = file.read(limit)
                return content if content else "(no content)"
        except FileNotFoundError:
            return "Error: File not found"
        except PermissionError:
            return "Error: Permission denied"
        except Exception as e:
            return f"Error: {e}"

class WriteFile(BaseTool):
    name = "writeFile"
    description = "Writes content to a specified file."
    schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to be written."
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file."
            }
        },
        "required": ["file_path", "content"]
    }

    def run(self, file_path: str, content: str) -> str:
        try:
            abs_path = safe_path(file_path)
            with open(abs_path, 'w') as file:
                file.write(content)
                return f"Successfully wrote to {abs_path}"
        except PermissionError:
            return "Error: Permission denied"
        except Exception as e:
            return f"Error: {e}"

class EditFile(BaseTool):
    name = "editFile"
    description = "Edits the content of a specified file."
    schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to be edited."
            },
            "old_content": {
                "type": "string",
                "description": "The old content to be replaced."
            },
            "new_content": {
                "type": "string",
                "description": "The new content to write to the file."
            }
        },
        "required": ["file_path", "old_content", "new_content"]
    }

    def run(self, file_path: str, old_content: str, new_content: str) -> str:
        try:
            abs_path = safe_path(file_path)
            with open(abs_path, 'r+') as file:
                content = file.read()
                if old_content not in content:
                    return "Error: Old content not found in the file"
                content = content.replace(old_content, new_content)
                file.seek(0)
                file.write(content)
                file.truncate()
                return f"Successfully edited {abs_path}"
        except FileNotFoundError:
            return "Error: File not found"
        except PermissionError:
            return "Error: Permission denied"
        except Exception as e:
            return f"Error: {e}"

