import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run the python file at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath leading to the target python file to execute.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    #create absolute filepaths for target and working directory
    working_directory_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    #return error if target is not in working directory
    if not target_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the working directory.'

    #if the target's directory does not exist return error string
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'

    #if the target does not have a .py extension return error string
    if not target_path[-3:] == '.py':
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        #execute the target python file with given args and capture the output
        result = subprocess.run(['uv', 'run', target_path] + args, capture_output=True, text=True, cwd=working_directory_path, timeout=30)
        
        #format a return string
        output = f'STDOUT: {result.stdout}STDERR: {result.stderr}'
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}'
        if output == '':
            output = 'No output produced'
        return output

    #check for errors and return error string if you find one
    except Exception as e:
        return f'Error: executing Python file {e}'
    

