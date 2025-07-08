import os
from config import MAX_FILE_CHARS


def get_file_content(working_directory, file_path):
    joined_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(joined_path)

    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_FILE_CHARS + 1)

            if len(file_content_string) > MAX_FILE_CHARS:
                file_content_string = file_content_string[:-1]
                file_content_string = (
                    file_content_string
                    + f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
                )
                return file_content_string
            else:
                return file_content_string

    except Exception as e:
        return f"Error: {e}"
