import os

def write_file(working_directory, file_path, content):
    joined_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(joined_path)

    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.path.exists(absolute_path)
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        with open(absolute_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error {e}'
