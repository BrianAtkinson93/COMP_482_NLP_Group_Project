import argparse
from utilities import gui
from models import model
from utilities.config import config
from utilities.utilities import *

# Dictionary of available models

model_name="gigabyte-1k-q4_0.gguf"


def main_local():
    """
    Runs the chat application with the local model.

    This function initializes the GUI, ensures the selected model exists, and sets up the chat interface.

    Args:
        args (Namespace): Command line arguments passed to the script.
    """
    # Initialize the GUI with the selected model
    chat_gui = gui.ChatGUI(model_name)

    # Download model if it does not exist
    ensure_model_exists(model_name)

    # Initialize the local GPT4All model
    chat_model = model.ChatModel_gpt4all(model_path='.\models', model_name=model_name)

    # Function to handle sending messages
    def send_message_wrapper():
        user_message = chat_gui.get_user_input()
        if user_message:
            response = chat_model.send_message(user_message)
            chat_gui.update_chat_history(f"User: {user_message}\n", 'user')
            chat_gui.update_chat_history(f"Bot: {response}\n", 'bot')

    # Set the action for sending messages and run the GUI
    chat_gui.set_send_message_action(send_message_wrapper)
    chat_gui.run()


def main_api(args):
    """
    Runs the chat application with the OpenAI API model.

    This function initializes the GUI with the OpenAI model and sets up the chat interface.

    Args:
        args (Namespace): Command line arguments passed to the script.
    """
    # Initialize the GUI with OpenAI model
    chat_gui = gui.ChatGUI(models[args.model][0])

    # Initialize the OpenAI API model
    chat_model = model.ChatModel_open_ai(config.config.api_key)

    # Function to handle sending messages
    def send_message_wrapper():
        user_message = chat_gui.get_user_input()
        if user_message:
            chat_gui.update_chat_history(f"User: {user_message}\n", 'user')
            response = chat_model.send_message(user_message)
            chat_gui.update_chat_history(f"Bot: {response}\n", 'bot')

    # Set the action for sending messages and run the GUI
    chat_gui.set_send_message_action(send_message_wrapper)
    chat_gui.run()


if __name__ == "__main__":
    main_local()
