from pprint import pprint
from openai import OpenAI

# Set the API key in .envrc file

client = OpenAI()

model = "gpt-3.5-turbo-0125"

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "Who won the NBA finals in 2020?"
    },
]

response = client.chat.completions.create(model=model, messages=messages).model_dump()
pprint(response)