import os

"""List contents of a directory and their sizes and is_dir values, checking that the target dir 
is inside of the working dir scope and a valid dir."""
def get_files_info(working_directory, directory="."):
    # create normalized absolute paths for working dir and target dir
    abs_work = os.path.normpath(os.path.abspath(working_directory))
    abs_target = os.path.normpath(os.path.abspath(os.path.join(working_directory, directory)))

    # check that the target path starts with the working dir path so that AI is working
    # in scope, and that target path and working path are not identical (which allows
    # AI to run this on the working dir without erroring out)
    if not abs_target.startswith(abs_work + os.sep) and abs_target != abs_work:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # check that the target path is a dir, error out if it is not
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'
    
    # try looping through each item in the target dir,
    # grabbing its name, path, size, is_dir,
    # and appending them in a formatted string to a list
    # that is then returned as a string separated by newlines. 
    # if an Exception is raised, return a formatted error string. 
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
