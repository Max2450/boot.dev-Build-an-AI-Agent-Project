import os
import subprocess
import sys
from google import genai
from google.genai import types

# Define the function schema for run_python_file to be used by the Gemini API
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath where the Python file is located, relative to the working directory.",
            ),
        },
    ),
)

"""Run a Python file within a specified working dir, ensuring the target file is inside the working dir scope."""
def run_python_file(working_directory, file_path, args=[]):

    # create normalized absolute paths for working dir and target file
    abs_work = os.path.normpath(os.path.abspath(working_directory))
    abs_target = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))

    # check that the target path starts with the working dir path so that AI is working
    # in scope, error out if it is not
    if not abs_target.startswith(abs_work + os.sep) and abs_target != abs_work:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # check that the target path is a file, error out if it is not
    if not os.path.exists(abs_target):
        return f'Error: File "{file_path}" not found.'

    # check that the target path is a Python file, error out if it is not
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    # try executing the Python file as a subprocess, capturing stdout and stderr and returning them. 
    try:
        cmd = [sys.executable, abs_target, *args]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=abs_work, timeout=30)
        output_stdout = result.stdout or ''
        output_stderr = result.stderr or ''
        output_combo = f"STDOUT:{output_stdout}\nSTDERR:{output_stderr}"

        # if the process exits with a non-zero code, return an error string with the code
        if result.returncode != 0:
            return f'{output_combo}\nProcess exited with code {result.returncode}'
        
        # if there is no output at all, return a message indicating that
        if output_stderr == '' and output_stdout == '':
            return f"No output produced."
        
        # otherwise return the combined output
        return output_combo
    
    # if a timeout occurs, return a timeout error string
    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out.'
    
    # if any other Exception is raised, return a formatted error string
    except Exception as e:
        return f'Error: executing Python file: {e}'