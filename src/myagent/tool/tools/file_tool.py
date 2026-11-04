import glob
from pathlib import Path

from pydantic import BaseModel, Field

from .basetool import BaseTool, safe_path


class GlobArgs(BaseModel):
    directory: str = Field(description="The directory to search in.")
    pattern: str = Field(description="The glob pattern to match files.")


class Glob(BaseTool):
    name = "glob"
    description = "List files in a directory matching a pattern."
    args_model = GlobArgs

    def run(self, directory: str, pattern: str) -> list[str]:
        try:
            # Ensure the directory is safe
            abs_directory = safe_path(directory)
            # Use glob to find matching files
            matched_files = glob.glob(str(abs_directory / pattern))
            return [str(Path(f).resolve()) for f in matched_files]
        except ValueError as ve:
            return [f"Error: {ve}"]
