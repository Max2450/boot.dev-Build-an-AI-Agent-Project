import os
import config
from google import genai
from google.genai import types

# Define the function schema for get_file_content to be used by the Gemini API
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Absolute or relative working directory to constrain file reading."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath where the file is located, relative to the working directory.",
            ),
        },
        required=["working_directory", "file_path"],
    ),
)

"""Read the content of a file within a specified working dir, ensuring the target file is inside the working dir scope and a regular file. 
If the file exceeds MAX_CHARS, truncate the output and indicate truncation"""
def get_file_content(working_directory, file_path):

    # create normalized absolute paths for working dir and target file
    abs_work = os.path.normpath(os.path.abspath(working_directory))
    abs_target = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))

    # check that the target path starts with the working dir path so that AI is working
    # in scope, error out if it is not
    if not abs_target.startswith(abs_work + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # check that the target path is a file, error out if it is not
    if not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # try opening and reading the file, returning its content
    try:
        with open(abs_target, 'r', encoding='utf-8') as f:
            chunk = f.read(config.MAX_CHARS + 1)

            # if the file exceeds MAX_CHARS, truncate the output and indicate truncation
            if len(chunk) > config.MAX_CHARS:
                return f'{chunk[:config.MAX_CHARS]}[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
        return chunk
    
    # if an Exception is raised, return a formatted error string
    except Exception as e:
        return f"Error: {e}"