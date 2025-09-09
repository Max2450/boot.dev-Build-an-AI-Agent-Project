import os
from dotenv import load_dotenv
from google import genai
import sys

def main():
    print("Hello from aiproject!")
    
    # fetch API key from project root dir and create a Gemini Client using it
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # check that API_KEY is not empty, if it is, exit.
    if api_key != False:
        client = genai.Client(api_key=api_key)
    else:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)

    # check for user inputted prompt, if none exists, raise Exception. 
    if len(sys.argv) < 2:
        print("No prompt provided")
        sys.exit(1)
    
    user_input = sys.argv[1]

    # send a prompt using gemini 2.0 flash
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=user_input)
    
    # print the response and token usage
    print(response.text)
    prompt_tokens_used = response.usage_metadata.prompt_token_count
    response_tokens_used = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {prompt_tokens_used}")
    print(f"Response tokens: {response_tokens_used}")

if __name__ == "__main__":
    main()
