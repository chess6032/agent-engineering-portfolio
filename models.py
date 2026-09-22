# list models available for your API key

from openai import OpenAI


def get_models(client): # pass in OpenAI()
    model_list = client.models.list()
    return [model.id for model in model_list.data]

def print_models(client):
    for modelID in get_models(client):
        print(modelID)

if __name__ == "__main__":
    print_models(OpenAI())
