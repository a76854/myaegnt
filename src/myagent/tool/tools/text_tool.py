from pydantic import BaseModel, Field

from .basetool import BaseTool, safe_path


class ReadFileArgs(BaseModel):
    file_path: str = Field(description="The path to the file to be read.")
    limit: int = Field(description="The maximum number of characters to read from the file.")


class ReadFile(BaseTool):
    name = "readFile"
    description = "Reads the content of a specified file."
    args_model = ReadFileArgs

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


class WriteFileArgs(BaseModel):
    file_path: str = Field(description="The path to the file to be written.")
    content: str = Field(description="The content to write to the file.")


class WriteFile(BaseTool):
    name = "writeFile"
    description = "Writes content to a specified file."
    args_model = WriteFileArgs

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


class EditFileArgs(BaseModel):
    file_path: str = Field(description="The path to the file to be edited.")
    old_content: str = Field(description="The old content to be replaced.")
    new_content: str = Field(description="The new content to write to the file.")


class EditFile(BaseTool):
    name = "edit"
    description = "Edits the content of a specified file."
    args_model = EditFileArgs

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
