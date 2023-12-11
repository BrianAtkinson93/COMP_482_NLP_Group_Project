import os
import subprocess
import requests
import platform
import sys

from tqdm import tqdm


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

    def check_and_install_git_lfs():
        try:
            # Check if Git LFS is installed
            subprocess.run(["git", "lfs", "version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Git LFS is already installed.")
        except subprocess.CalledProcessError:
            # Git LFS is not installed, proceed with installation
            print("Installing Git LFS...")

            if platform.system() == "Linux":
                # Try to identify the package manager and install Git LFS
                package_managers = {
                    "apt-get": ["sudo", "apt-get", "install", "git-lfs"],
                    "yum": ["sudo", "yum", "install", "git-lfs"],
                    "dnf": ["sudo", "dnf", "install", "git-lfs"],
                    "pacman": ["sudo", "pacman", "-S", "git-lfs"],
                    "zypper": ["sudo", "zypper", "install", "git-lfs"]
                }

                for manager, command in package_managers.items():
                    if subprocess.run(["which", manager], stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).returncode == 0:
                        subprocess.run(command, check=True)
                        print(f"Git LFS installed successfully with {manager}.")
                        break
                else:
                    print("No compatible package manager found. Please install Git LFS manually.")
            elif platform.system() == "Windows":
                subprocess.run(["git", "lfs", "install"], check=True)
                print("Git LFS installed successfully.")
            else:
                print("Unsupported operating system.")
                sys.exit(1)

    check_and_install_git_lfs()

    model_path = f'./models/{model_name}'
    if not os.path.exists(model_path):
        print(f"Downloading model: {model_name}")
        response = requests.get(download_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()
        print(f"Model downloaded: {model_name}")
    else:
        print(f"Model already exists: {model_name}")


def ensure_models_exist(which):
    """
    Ensures that the specified models exist in the local directory, downloading them if necessary.

    Args:
        which (tuple): A tuple containing the keys of the models to be checked and downloaded if necessary.

    Returns:
        None: This function does not return anything.
    """
    model_urls = {
        "nous_hermes": (
            "nous-hermes-llama2-13b.Q4_0.gguf", "https://gpt4all.io/models/gguf/nous-hermes-llama2-13b.Q4_0.gguf"),
        "mistral": ("mistral-7b-openorca.Q4_0.gguf", "https://gpt4all.io/models/gguf/mistral-7b-openorca.Q4_0.gguf"),
        "mistral_2": (
            "mistral-7b-instruct-v0.1.Q4_0.gguf", "https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf"),
        "wizard": ("wizardlm-13b-v1.2.Q4_0.gguf", "https://gpt4all.io/models/gguf/wizardlm-13b-v1.2.Q4_0.gguf"),
        "Brian-Mason": ("gigabyte-1k-q4_0.gguf", "https://huggingface.co/masonym/gigabyte-1k-q4_0-GGUF/resolve/main/gigabyte-1k-q4_0.gguf?download=true")
    }

    download_model(*model_urls[which[0]])
