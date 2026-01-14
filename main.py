import os
import sys
import argparse

from call_function import available_functions, call_function
from prompts import system_prompt
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

    for _ in range(20):
        # Send and receive response from gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

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

        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)

                if not function_call_result.parts:
                    raise Exception("Empty parts list")
                if not function_call_result.parts[0].function_response:
                    raise Exception("No function response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("No result")

                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            return

    print("Error: Agent could not produce reponse in 20 attempts")
    sys.exit(1)


if __name__ == "__main__":
    main()
