from .get_file_content import get_file_content
from .run_python import run_python_file
from .write_file import write_file
from .get_files_info import get_files_info
from google.genai import types

function_dict = {
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
    "get_files_info": get_files_info
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    print(f" - Calling function: {function_call_part.name}")

    function_object = function_dict[function_call_part.name]
    if not function_call_part.name in function_dict:
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name, # Use function_call_part.name here
                        response={"error": f"Unknown function: {function_call_part.name}"}, # And here
                    )
                ],
            )
    
    function_call_dict = {
        "working_directory": "./calculator",
         **function_call_part.args
    }

    response = function_object(**function_call_dict)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": response},
        )
    ],
)