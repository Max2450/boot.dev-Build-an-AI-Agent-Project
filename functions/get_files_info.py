import os

def get_files_info(working_directory, directory="."):
    # full_path = os.path.join(working_directory, directory)
    abs_work = os.path.normpath(os.path.abspath(working_directory))
    abs_target = os.path.normpath(os.path.abspath(os.path.join(working_directory, directory)))

    if not abs_target.startswith(abs_work + os.sep) and abs_target != abs_work:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'
    
    try:
        line_list = []
        for item in os.listdir(abs_target):
            filename = item
            path = os.path.join(abs_target, item)
            filesize = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            line_list.append(f"- {filename}: file_size={filesize} bytes, is_dir={is_dir}")
        return '\n'.join(line_list)
    except Exception as e:
        return f"Error: {e}"
