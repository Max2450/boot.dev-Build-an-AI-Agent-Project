import os
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from aiproject!")
    
    # fetch API key from project root dir and create a Gemini Client using it
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # send a prompt using gemini 2.0 flash
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    
    # print the response and token usage
    print(response.text)
    prompt_tokens_used = response.usage_metadata.prompt_token_count
    response_tokens_used = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {prompt_tokens_used}")
    print(f"Response tokens: {response_tokens_used}")

if __name__ == "__main__":
    main()
