import os

def write_file(working_directory, file_path, content):
    #create absolute filepaths for target and working directory
    working_directory_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    #return error if target is not in working directory
    if not target_path.startswith(working_directory_path):
        return f'Error: cannot read {file_path} as it is outside the working directory'
    
    #if the current target file does not exist create it
    if not os.path.exists(os.path.dirname(target_path)):
        try:
            os.makedirs(os.path.dirname(target_path))
        except Exception as e:
            return f'Error creating directory: {e}'
        
    try:
        with open(target_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error writing to file: {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
