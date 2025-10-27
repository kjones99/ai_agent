import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():
    #load dotenv function which allows us to pull the API key from .env
    load_dotenv()

    #store user prompts from argv parsing out the script name
    args = sys.argv[1:]
    verbose_flag = False

    #if no user input is found print print an error message to console and exit with code 1
    if not args:
        print('AI Code Assisstant')
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a to-do list app?"')
        sys.exit(1)

    if '--verbose' in args:
        args.remove('--verbose')
        verbose_flag = True

    #pull the API key from .env and create a client using that API key
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    #if user input was found join all the prompts with " " and create a list that will store the entire conversation with the LLM
    user_prompt = " ".join(args)
    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    #call the generate content function
    generate_content(client, messages, verbose_flag)

def generate_content(client, messages, verbose_flag):
    #pass the user prompts list to the specific AI model and store response object
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        )
    
    #print the LLM's response to console
    print("Response:\n", response.text)

    #if user included the verbose flag also print the # of Prompt and Response tokens the user currently has
    if verbose_flag:
        print("User prompt:", messages[-1].parts[-1].text)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)




if __name__ == "__main__":
    main()
