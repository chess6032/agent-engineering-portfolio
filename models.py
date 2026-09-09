# list models available for your API key

from openai import OpenAI

# The client automatically picks up the OPENAI_API_KEY environment variable,
# or you can pass it explicitly: client = OpenAI(api_key="YOUR_API_KEY")
client = OpenAI()

# Fetch the list of available models
model_list = client.models.list()

# Print out just the model IDs
for model in model_list.data:
    print(model.id)
