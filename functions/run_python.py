import os
import subprocess

def run_python_file(working_directory, file_path):
    joined_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(joined_path)

    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(absolute_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        subprocess_value = subprocess.run(f'uv run {file_path}',cwd=os.path.abspath(working_directory), capture_output=True, text=True, timeout=30, shell=True)
        result_string = f'STDOUT: {subprocess_value.stdout} STDERR: {subprocess_value.stderr}'
        if not subprocess_value.stderr.strip() and not subprocess_value.stdout.strip():
            return f'No output produced.'
        if subprocess_value.returncode != 0:
            result_string = result_string + f' Process exited with code {subprocess_value.returncode}'

        return result_string
        
    except Exception as e:
        return f"Error: executing Python file: {e}"


