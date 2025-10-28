import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import call_function, available_functions

MODEL = "gemini-2.0-flash-001"
MAX_ITERATIONS = 20

def main():
    #load dotenv function which allows us to pull the API key from .env
    load_dotenv()

    verbose_flag = '--verbose' in sys.argv

    #store user prompts from argv parsing out the script name
    args = sys.argv[1:]
    if '--verbose' in args:
        args.remove('--verbose')
        verbose_flag = True

    #if no user input is found print print an error message to console and exit with code 1
    if not args:
        print('AI Code Assisstant')
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a to-do list app?"')
        sys.exit(1)

    #pull the API key from .env and create a client using that API key
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    #if user input was found join all the prompts with " " and create a list that will store the entire conversation with the LLM
    user_prompt = " ".join(args)

    if verbose_flag:
        print(f'User prompt: {user_prompt}')

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    #call the generate content function
    i = 0
    while True:
        i += 1
        if i > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose_flag)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose_flag):
    #pass the user prompts list to the specific AI model and store response object
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
            ),
        )
    
    if verbose_flag:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    #iterate through the response candidates and add them to the messages list
    for candidate in response.candidates:  
        function_call_holder = candidate.content
        if function_call_holder:  
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text
    #If the response includes function calls impliment those calls and store the result
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose_flag)

        if not function_call_result:
            raise Exception(f'no result from calling \"{function_call_part.name}\" with args \"{function_call_part.args}\"')

        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            ):
                raise Exception ("empty function call result")
        
        #add the types.Content object to function_responses list
        function_responses.append(function_call_result.parts[0])

    #if your function_responses list is empty there was no response from the function call 
    if not function_responses:
        raise Exception('no function responses generated, exiting.')
    
    messages.append(types.Content(role='user', parts=function_responses))
    


if __name__ == "__main__":
    main()
