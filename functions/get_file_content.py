import os
from config import MAX_CHARS

from google.genai import types


def get_file_content(working_directory, file_path):
    try:

        working_dir_abspath = os.path.abspath(working_directory)
        target_file = os.path.join(working_dir_abspath, file_path)

        valid_target_file = (
            os.path.commonpath([working_dir_abspath, target_file])
            == working_dir_abspath
        )

        if not valid_target_file:
            return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: '{file_path}'"

        content = ""

        with open(target_file, "r") as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += (
                    f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"
                )
        return content

    except Exception as e:
        return f"Error: {e.with_traceback}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads content from file up to 10,000 characters, if the file is larger it returns the maximum allowed charactersand appends an error explaining the truncation of the output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to read from",
            )
        },
        required=["file_path"],
    ),
)
