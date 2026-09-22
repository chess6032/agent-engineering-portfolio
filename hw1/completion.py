import os
import sys

from openai import OpenAI

from usage import print_usage

if __name__ == "__main__":
    model = os.environ.get('model')
    model = model if model else "gpt-5.4-mini"

    fmt = os.environ.get('format')

    client = OpenAI()

    print(f"Using model {model}")
    print('-------- Enter your prompt: --------')

    userText = ''
    while True:
        try:
            line = input()
        except EOFError:
            break
        userText += '\n' + line

    if not userText:
        exit(0)
    
    print('-------- Processing... --------')

    preamble = "(Fully answer the following prompt to the best of your ability **in one response**. " \
        + "Do not ask for further input from the user or anticipate further conversation in any way. " \
        + "Respond in plain text, with no Markdown formatting.)\n"

    inputText = preamble + userText

    response = client.responses.create(
        model=model,
        input=inputText,
    )

    print()
    print(response.output_text)
    print_usage(model=model, usage=response.usage)
