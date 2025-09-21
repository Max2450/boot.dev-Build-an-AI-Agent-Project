import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import config
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content 
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

# Load the system prompt from the config module
system_prompt = config.SYSTEM_PROMPT

# Register the function schemas in a Tool object to make it available for the Gemini API
# This allows the AI to call this function when needed.
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# Create a configuration object for the Gemini API that includes the available functions
# and the system instruction to guide the AI's behavior.
genai_config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

def main():
    
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
    
    # set user_input to the first argument after the script name
    user_input = sys.argv[1]

    # create a list of types.content, setting the user's input as the only message for now
    messages = [types.Content(role="user", parts=[types.Part(text=user_input)])]

    # loop for up to 20 iterations to allow the AI to call functions multiple times if needed
    for i in range(config.MAX_GENERATION_ITERATIONS):
        try:

            print(f"\n--- Generation Iteration {i+1} ---")

            # send a prompt using gemini 2.0 flash, passing in the list of user messages
            # also pass in the available functions and config object
            # this makes the functions available to the Gemini model
            response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=genai_config)
            
            # if verbose tag used, print tokens used and prompt used
            if response and verbose:
                prompt_tokens_used = response.usage_metadata.prompt_token_count
                response_tokens_used = response.usage_metadata.candidates_token_count
                print(f"User prompt: {user_input}")
                print(f"Prompt tokens: {prompt_tokens_used}")
                print(f"Response tokens: {response_tokens_used}")

            # appending candidate content to the messages list
            for candidate in response.candidates:
                messages.append(candidate.content)

            # if the response contains a function call, handle it
            if response.function_calls and len(response.function_calls) > 0:
                from function_call import call_function
                function_call_result = call_function(response.function_calls[0], verbose=verbose)
                
                # validate structure of function_call_result
                if (
                    not function_call_result.parts
                    or not hasattr(function_call_result.parts[0], "function_response")
                    or not hasattr(function_call_result.parts[0].function_response, "response")
                ):
                    # raise an Exception if the structure is not as expected
                    raise Exception("Invalid function call result structure.")
                
                # if verbose flag is set, print additional info
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                # append the function call response to the messages list
                messages.append(types.Content(
                    role="user",
                    parts=[
                        types.Part(function_response=function_call_result.parts[0].function_response)
                    ]
                ))
                continue  # continue to the next iteration to get a new response after the function call
                
            elif response.text:
                print(response.text)
                break  # exit the loop if a final text response is received

            # if no other path, print a message and break the loop
            else:
                print("No function call or text response received.")
                break
        
        # catch any other Exception and print it, then break the loop
        except Exception as e:
            print(f"Error during iteration {i+1}: {e}")
            break

if __name__ == "__main__":
    main()
