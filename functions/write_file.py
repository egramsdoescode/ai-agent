import os

from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_dir_abspath = os.path.abspath(working_directory)
        target_file = os.path.join(working_dir_abspath, file_path)

        valid_target_file = (
            os.path.commonpath([working_dir_abspath, target_file])
            == working_dir_abspath
        )

        if not valid_target_file:
            return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"

        if os.path.isdir(target_file):
            return f"Error: Cannot write to '{file_path}' as it is a directory"

        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_file, "w") as file:
            file.write(content)

        return (
            f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to <content> to file with specified <file_path>",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be written to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to file",
            ),
        },
        required=["file_path", "content"],
    ),
)
