import os
import sys
from gpt4all import GPT4All

models = {
    1: ("nous_hermes", "models/nous-hermes-llama2-13b.Q4_0.gguf"),
    2: ("mistral", "models/mistral-7b-openorca.Q4_0.gguf")
}

# Select the model to use
m2u = models[1]

# Define the path, model name, and deny downloads
model = GPT4All(model_path="./models", model_name=m2u[1], allow_download=False)

# Start session with model
with model.chat_session():
    assert model.current_chat_session[0]['role'] == 'system'
    question = "What is the capital of France?"
    print(f'User: {question}')
    output = model.generate(question, max_tokens=10)
    print(f'Bot: {output}')
    question_2 = "Where in canada is the capital?"
    print(f'User: {question_2}')
    output = model.generate(question_2, max_tokens=10)
    print(f'Bot: {output}')
    sys.exit()
