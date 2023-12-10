import os
import requests
import sys


def read_documents(folder_path):
    """
    Reads all text files in a specified folder and returns their contents.

    Args:
        folder_path (str): The path to the folder containing text files.

    Returns:
        dict: A dictionary where keys are filenames and values are the contents of the files.
    """
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents


import os


def get_system_username():
    """
    Retrieves the username of the current system user.

    Returns:
        str: The username of the current system user. Returns 'Unknown User' if an error occurs.
    """
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
    """
    Downloads a model file from a given URL into a local directory.

    Args:
        model_name (str): The name of the model to be downloaded.
        download_url (str): The URL from where the model can be downloaded.

    Returns:
        None: This function does not return anything. It prints messages indicating the download status.
    """
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


def ensure_model_exists(model_name):
    """
    Ensures that the model exists in the local directory, downloading if necessary.

    Args:
        which (tuple): A tuple containing the keys of the models to be checked and downloaded if necessary.

    Returns:
        None: This function does not return anything.
    """
    model_url = "https://huggingface.co/masonym/gigabyte-1k-q4_0-GGUF/resolve/main/gigabyte-1k-q4_0.gguf?download=true"

    download_model(model_name, model_url)
