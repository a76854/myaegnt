from .basetool import BaseTool, safe_path


class Glob(BaseTool):
    name = "glob"
    description = "List files in a directory matching a pattern."
    schema = {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to search in."
            },
            "pattern": {
                "type": "string",
                "description": "The glob pattern to match files."
            }
        },
        "required": ["directory", "pattern"]
    }

    def __init__(self):
        pass

    def run(self, directory: str, pattern: str) -> list:
        import glob
        from pathlib import Path
        try:
            # Ensure the directory is safe
            abs_directory = safe_path(directory)
            # Use glob to find matching files
            matched_files = glob.glob(str(abs_directory / pattern))
            return [str(Path(f).resolve()) for f in matched_files]
        except ValueError as ve:
            return [f"Error: {ve}"]
