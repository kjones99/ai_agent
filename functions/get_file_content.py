import os
from config import MAX_CHARS
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="List the first 10000 characters in the file specified by the file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath leading to the target file to read characters from.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    #create absolute filepaths for target and working directory
    working_directory_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    #return error if target is not in working directory
    if not target_path.startswith(working_directory_path):
        return f'Error: cannot read {file_path} as it is outside the working directory'
    
    #return error if target path doesnt lead to a file
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: {file_path}'
    
    try:
        #read from the target file until the MAX_CHARS limit is reached
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        
        #If you read in MAX_CHARS let the user know the file content was truncated
        if len(file_content_string) == MAX_CHARS:
            file_content_string += f'[...File {file_path} truncated at {MAX_CHARS} characters]'
       
        #return the file content unless you found an error along the way
        return file_content_string
    except Exception as e:
        f'Error listing file contents: {e}'