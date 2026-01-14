import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abspath = os.path.abspath(working_directory)
        target_file = os.path.join(working_dir_abspath, file_path)

        valid_target_file = os.path.commonpath(
            [working_dir_abspath, target_file]
        ) == working_dir_abspath and working_dir_abspath == os.path.dirname(target_file)

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        completed_process = subprocess.run(
            command, cwd=os.path.dirname(target_file), capture_output=True, timeout=30
        )

        result = ""

        if completed_process.returncode != 0:
            result += f"Process exited with code {completed_process.returncode}\n"

        if not completed_process.stdout and not completed_process.stderr:
            result += "No output produced\n"
        else:
            result += f"STDOUT: {completed_process.stdout}\n"
            result += f"STDERR: {completed_process.stderr}\n"

        return result
    except Exception as e:
        return f"Error: excecuting Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file specified in <file_path> with optional arguments [args]",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to Python file to be executed",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING, description="Individual argument"
                ),
                description="Optional arguments to be run with the Python file",
            ),
        },
        required=["file_path"],
    ),
)
