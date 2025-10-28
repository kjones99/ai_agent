❗ This Agent can run arbitrary python code. It is for learning purposes only. Use at your own risk.

This is a toy version of claude code and utilizes the Gemini API to create modify and run files within a designated subdirectory

To enable functionality the user will have to make an account with Google Gemini and save their API key in a ".env" file in the root directory.  This key should be saved in the format GEMINI_API_KEY="{your-key-here}"

Then the user will then have to activate the venv by the command "source .venv/bin/activate"

As it stands the AI has the ability to view, modify, and create files within the ./calculator subdirectory
and you can make calls to it in the fashion  uv run main.py '{your_prompt_here}'


