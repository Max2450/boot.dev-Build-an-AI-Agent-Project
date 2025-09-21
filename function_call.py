from google import genai
from google.genai import types

# This function takes a function call part (which includes the function name and arguments)
# and calls the appropriate function based on the function name.
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    # Add a working_directory argument to the function args, set to the calculator directory
    # This ensures that all file operations are constrained to this directory for security
    # and to prevent the AI from accessing files outside of this directory.
    function_args['working_directory'] = './calculator' 

    # Print the function call details if verbose is enabled
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
        
    # if not verbose, just print the function name
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Call the appropriate function based on the function name
    if function_name == "get_files_info":
        from functions.get_files_info import get_files_info
        function_result = get_files_info(**function_args)

    elif function_name == "get_file_content":
        from functions.get_file_content import get_file_content
        function_result = get_file_content(**function_args)

    elif function_name == "run_python_file":
        from functions.run_python_file import run_python_file
        function_result = run_python_file(**function_args)

    elif function_name == "write_file":
       from functions.write_file import write_file
       function_result = write_file(**function_args)

    # If the function name is not recognized, return an error message
    else:
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
    
    # Return the function result wrapped in a types.Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )