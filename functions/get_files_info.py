import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get content of the specific file from the file path, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to specific file to list content from, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the script from the file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to specific script to execute, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the file in the specified directory with the provided content, constrained to the working directory. Create file if it does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to specific file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the specific file",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."

    joined_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(joined_path)

    wd_abs = os.path.abspath(working_directory)
    wd_check = wd_abs if wd_abs.endswith(os.sep) else wd_abs + os.sep

    if not (absolute_path + os.sep).startswith(wd_check):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'

    try:
        dir_list = os.listdir(absolute_path)
        file_info_list = []
        for item in dir_list:
            file_info = f"- {item}: file_size={os.path.getsize(os.path.join(absolute_path, item))} bytes, is_dir={os.path.isdir(os.path.join(absolute_path, item))}"
            file_info_list.append(file_info)
        return "\n".join(file_info_list)
    except Exception as e:
        return f"Error: {e}"
