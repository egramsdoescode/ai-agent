import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # load secrets
    load_dotenv()

    # Load in API key from secrets
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("api key not found")

    # Gather user prompt
    parser = argparse.ArgumentParser(description="AiChatBot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Generate client to comminicate with gemini
    client = genai.Client(api_key=api_key)

    # Send and receive response from gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )

    if not response.usage_metadata:
        raise RuntimeError("usage_metadata not found")

    if args.verbose:
        print(
            f"""
User prompt: {args.user_prompt}
Prompt tokens: {response.usage_metadata.prompt_token_count}
Response tokens: {response.usage_metadata.candidates_token_count}
            """
        )
    print(response.text)


if __name__ == "__main__":
    main()
