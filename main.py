import argparse
import threading

from utilities import gui
from models import model
from utilities.config import config
from utilities.utilities import *

# Dictionary of available models
models = {
    1: ("nous_hermes", "nous-hermes-llama2-13b.Q4_0.gguf"),
    2: ("mistral", "mistral-7b-openorca.Q4_0.gguf"),
    3: ("mistral_2", "mistral-7b-instruct-v0.1.Q4_0.gguf"),
    4: ("wizard", "wizardlm-13b-v1.2.Q4_0.gguf"),
    5: ("Brian-Mason", "gigabyte-1k-q4_0.gguf")
}


def main_local(args):
    """
    Runs the chat application with a local GPT4All model.

    This function initializes the GUI, ensures the selected model exists, and sets up the chat interface.

    Args:
        args (Namespace): Command line arguments passed to the script.
    """
    # Initialize the GUI with the selected model
    chat_gui = gui.ChatGUI(models[args.model][0])

    # Download model if it does not exist
    ensure_models_exist(models[args.model])

    # print(models[args.model][1])
    # sys.exit(8)
    # Initialize the local GPT4All model
    chat_model = model.ChatModelGpt4All(model_path='./models', model_name=models[args.model][1], allow_download=True)

    def send_message_wrapper():
        user_message = chat_gui.get_user_input()
        if user_message:
            chat_gui.update_chat_history(f"User: {user_message}\n", 'user')
            chat_gui.show_loading_indicator()  # Show loading indicator

            def handle_response():
                response = chat_model.send_message(user_message)
                chat_gui.window.after(0, lambda: chat_gui.update_chat_history(f"Bot: {response}\n", 'bot'))
                chat_gui.window.after(0, chat_gui.hide_loading_indicator)  # Hide loading indicator

            threading.Thread(target=handle_response).start()

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
    chat_model = model.ChatModel_open_ai(config.api_key)

    def send_message_wrapper():
        user_message = chat_gui.get_user_input()
        if user_message:
            # Update the chat history immediately with the user's message
            chat_gui.update_chat_history(f"User: {user_message}\n", 'user')

            # Function to handle model response
            def handle_model_response():
                response = chat_model.send_message(user_message)
                chat_gui.update_chat_history(f"Bot: {response}\n", 'bot')

            # Start a new thread for model response
            response_thread = threading.Thread(target=handle_model_response)
            response_thread.start()

    # Set the action for sending messages and run the GUI
    chat_gui.set_send_message_action(send_message_wrapper)

    chat_gui.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Define command-line arguments
    parser.add_argument('-a-', '--api', default=False, action='store_true',
                        help='Use this flag to run with the OpenAI API model.')
    parser.add_argument("-m", '--model', type=int, default=5, choices=[1, 2, 3, 4, 5],
                        help="Choose a model number for the local GPT4All model.")

    # Parse arguments
    arguments = parser.parse_args()

    # Run the appropriate main function based on the arguments
    if arguments.api:
        main_api(arguments)
    else:
        main_local(arguments)
