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

    userText = sys.stdin.read()

    print('-------- Processing... --------')

    if not userText:
        exit(0)

    inputText = ('' if fmt else '(Respond in plain text, with no Markdown formatting.) ') + userText

    response = client.responses.create(
        model=model,
        input=inputText,
    )

    print()
    print(response.output_text)
    print_usage(model=model, usage=response.usage)
