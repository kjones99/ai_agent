import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write the given content into a file at the given filepath, creating it if it does not exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath leading to the target file to write the content to.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    #create absolute filepaths for target and working directory
    working_directory_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    #return error if target is not in working directory
    if not target_path.startswith(working_directory_path):
        return f'Error: cannot read {file_path} as it is outside the working directory'
    
    #if the target directory does not exist create it
    if not os.path.exists(os.path.dirname(target_path)):
        try:
            os.makedirs(os.path.dirname(target_path))
        except Exception as e:
            return f'Error creating directory: {e}'
        
    #write the content string to the target file   
    try:
        with open(target_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error writing to file: {e}'
    
    #if you were successful return a string indicating this
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
