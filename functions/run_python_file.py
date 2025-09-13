import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    abs_work = os.path.normpath(os.path.abspath(working_directory))
    abs_target = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))

    if not abs_target.startswith(abs_work + os.sep) and abs_target != abs_work:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_target):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        cmd = [sys.executable, abs_target, *args]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=abs_work, timeout=30)
        output_stdout = result.stdout or ''
        output_stderr = result.stderr or ''
        output_combo = f"STDOUT:{output_stdout}\nSTDERR:{output_stderr}"

        if result.returncode != 0:
            return f'{output_combo}\nProcess exited with code {result.returncode}'
        
        if output_stderr == '' and output_stdout == '':
            return f"No output produced."
        
        return output_combo
    
    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out.'
    except Exception as e:
        return f'Error: executing Python file: {e}'