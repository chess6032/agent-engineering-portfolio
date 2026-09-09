import os
from openai import OpenAI

from usage import print_usage

if __name__ == "__main__":
    model = os.environ.get('model')
    model = model if model else "gpt-5.4-mini"

    nofmt = os.environ.get('noformat')

    client = OpenAI()

    print(f"Using model {model}")
    userText = input('Enter your prompt:\n')

    if not userText:
        exit(0)

    inputText = ('(Respond in plain text, with no Markdown formatting.) ' if nofmt else '') + userText

    response = client.responses.create(
        model=model,
        input=inputText,
    )

    print()
    print(response.output_text)
    print_usage(model=model, usage=response.usage)
