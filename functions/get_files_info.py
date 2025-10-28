import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    #create the absolute file path for both the working directory and the target directory
    target_path = os.path.abspath(os.path.join(working_directory, directory))
    wd_target_path = os.path.abspath(working_directory)

    #if the target is not within the working directory return error
    if not target_path.startswith(wd_target_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #if the target is not a directory return error
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'
    
    #try except to catch standard library errors
    try:

        #store a list of items in the target directory and create a list to store info about those items
        contents = os.listdir(target_path)
        content_strings = [] 

        #iterate over the items in directory, get byte size and whether the item is a directory
        for item in contents:
            size = os.path.getsize(os.path.abspath(os.path.join(target_path, item)))
            is_dir = os.path.isdir(os.path.abspath(os.path.join(target_path, item)))
            
            #store a string with this info in the list content_strings
            content_strings.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')
        
        #join all the info strings into one return string
        return '\n'.join(content_strings)
    
    #or return an error message if we failed
    except Exception as e:
        return f'Error listing files: {e}'