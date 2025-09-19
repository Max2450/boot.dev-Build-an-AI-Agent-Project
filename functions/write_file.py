import os

"""Write content to a file within a specified working dir, ensuring the target file is inside the working dir scope."""
def write_file(working_directory, file_path, content):
    
    # create normalized absolute paths for working dir and target file
    abs_work = os.path.normpath(os.path.abspath(working_directory))
    abs_target = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))
    
    # check that the target path starts with the working dir path so that AI is working
    # in scope, error out if it is not
    if not abs_target.startswith(abs_work + os.sep):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # ensure the target directory exists, create it if it does not
    if not os.path.exists(file_path):
        dir_name = os.path.dirname(abs_target)
        if dir_name and not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)

            # if an Exception is raised, return a formatted error string
            except Exception as e:
                return f"Error: {e}"
            
    # try opening and writing to the file, returning a success message with number of characters written
    try:
        with open(abs_target, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    # if an Exception is raised, return a formatted error string
    except Exception as e:
        return f"Error: {e}"