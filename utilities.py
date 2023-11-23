import os
import requests
import sys


def read_documents(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents


import os


def get_system_username():
    try:
        user_name = os.getlogin()
    except Exception as e:
        user_name = 'Unknown User'
        print(f"Error getting system username: {e}")
    return user_name


# # Usage
# username = get_system_username()
# print(f"The system username is: {username}")


def download_model(model_name, download_url):
    model_path = f'./models/{model_name}'
    if not os.path.exists(model_path):
        print(f"Downloading model: {model_name}")
        response = requests.get(download_url, stream=True)
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Model downloaded: {model_name}")
    else:
        print(f"Model already exists: {model_name}")


def ensure_models_exist(which):
    model_urls = {
        "nous_hermes": (
            "nous-hermes-llama2-13b.Q4_0.gguf", "https://gpt4all.io/models/gguf/nous-hermes-llama2-13b.Q4_0.gguf"),
        "mistral": ("mistral-7b-openorca.Q4_0.gguf", "https://gpt4all.io/models/gguf/mistral-7b-openorca.Q4_0.gguf"),
        "mistral_2": (
            "mistral-7b-instruct-v0.1.Q4_0.gguf", "https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf"),
        "wizard": ("wizardlm-13b-v1.2.Q4_0.gguf", "https://gpt4all.io/models/gguf/wizardlm-13b-v1.2.Q4_0.gguf")
    }

    download_model(*model_urls[which[0]])
