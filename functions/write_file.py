import os

def write_file(working_directory, file_path, content):
    abs_work = os.path.normpath(os.path.abspath(working_directory))
    abs_target = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))
    
    if not abs_target.startswith(abs_work + os.sep):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_path):
        dir_name = os.path.dirname(abs_target)
        if dir_name and not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
            except Exception as e:
                return f"Error: {e}"

    try:
        with open(abs_target, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"