import os
import config

def get_file_content(working_directory, file_path):
    abs_work = os.path.normpath(os.path.abspath(working_directory))
    abs_target = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))

    if not abs_target.startswith(abs_work + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_target, 'r', encoding='utf-8') as f:
            chunk = f.read(config.MAX_CHARS + 1)
            if len(chunk) > config.MAX_CHARS:
                return f'{chunk[:config.MAX_CHARS]}[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
        return chunk
    except Exception as e:
        return f"Error: {e}"