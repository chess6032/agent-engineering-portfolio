from openai import OpenAI
import os

model = os.environ.get('model')
model = model if model else "gpt-5.4-mini"

client = OpenAI()

print(f"Using model {model}")
inputText = input('Enter your prompt:\n')

if not inputText:
    exit(0)

response = client.responses.create(
    model=model,
    input=inputText,
)

print(response.output_text)