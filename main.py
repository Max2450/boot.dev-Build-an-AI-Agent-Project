import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import config
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file, available_functions, config as functions_config

def main():
    #print("Hello from aiproject!")
    #print("=====Printing sys.argv for debugging=====")
    #print(sys.argv)
    
    # fetch API key from project root dir and create a Gemini Client using it
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # check that API_KEY is not empty or None, if it is, exit.
    if not api_key:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)
    client = genai.Client(api_key=api_key)
        
    # check for user inputted prompt, if none exists, raise Exception. 
    if len(sys.argv) < 2:
        print("No prompt provided")
        sys.exit(1)

    # check for verbose flag, set to True if it's in the 2nd index or later
    verbose = False
    if len(sys.argv) > 2:
        if '--verbose' in sys.argv[2:]:
            verbose = True
    
    user_input = sys.argv[1]

    # create a list of types.content, setting the user's input as the only message for now
    messages = [types.Content(role="user", parts=[types.Part(text=user_input)])]

    # send a prompt using gemini 2.0 flash, passing in the list of user messages
    # also take in system prompt from config.py
    # also pass in the available functions and config object created in get_files_info.py
    # this makes the get_files_info function available to the Gemini model
    system_prompt = config.SYSTEM_PROMPT
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))
    
    # if the response contains a function call, print the function name and args
    function_call_part = response.function_calls[0] if response.function_calls else None
    if response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    else:
        # print the response
        print(response.text)
    
    # if verbose tag used, print tokens used and prompt used
    if response and verbose:
        prompt_tokens_used = response.usage_metadata.prompt_token_count
        response_tokens_used = response.usage_metadata.candidates_token_count
        print(f"User prompt: {user_input}")
        print(f"Prompt tokens: {prompt_tokens_used}")
        print(f"Response tokens: {response_tokens_used}")

if __name__ == "__main__":
    main()
