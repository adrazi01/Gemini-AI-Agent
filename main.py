import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import available_functions 
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
verbose = "--verbose" in sys.argv
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("Error")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
]

if len(sys.argv) > 2 and sys.argv[2] == '--verbose':
    print("User prompt:", messages[0].parts[0].text)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

for iteration in range(20):
    try:
        response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
        for candidate in response.candidates:
            messages.append(candidate.content)
            finished = True
            for part in candidate.content.parts:
                if part.function_call != None:
                        result = call_function(part.function_call, verbose)
                        messages.append(types.Content(
                            role="tool",
                            parts=[
                                types.Part.from_function_response(
                                    name=part.function_call.name,
                                    response={"result": result},
                                )
                            ],
                        ))
                        finished = False
            if finished:
                text_reply = " ".join(
                getattr(part, "text", "") for part in candidate.content.parts if hasattr(part, "text")
                )
                print("Final response:", text_reply)
                break
        if finished:
            break
    except Exception as e:
        print(f"An error occured: {e}")

            
            





