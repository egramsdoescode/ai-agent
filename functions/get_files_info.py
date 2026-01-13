import os
from os.path import abspath


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
