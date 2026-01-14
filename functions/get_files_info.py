import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    try:

        working_dir_abspath = os.path.abspath(working_directory)
        target_dir = os.path.join(working_dir_abspath, directory)

        valid_target_dir = (
            os.path.commonpath([working_dir_abspath, target_dir]) == working_dir_abspath
        )

        if not valid_target_dir:
            return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

        if not os.path.isdir(target_dir):
            return f"Error: '{directory}' is not a directory"

        dir_info = ""

        for file in os.listdir(target_dir):
            path = os.path.join(target_dir, file)
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            dir_info += f"\t- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return dir_info

    except Exception as e:
        return f"Error: '{e.with_traceback}'"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            )
        },
    ),
)
