import argparse
import gui
import model
import config

from utilities import *

# Dictionary of available models
models = {
    1: ("nous_hermes", "nous-hermes-llama2-13b.Q4_0.gguf"),
    2: ("mistral", "mistral-7b-openorca.Q4_0.gguf"),
    3: ("mistral_2", "mistral-7b-instruct-v0.1.Q4_0.gguf"),
    4: ("wizard", "wizardlm-13b-v1.2.Q4_0.gguf")
}


def main_local(args):
    # Initialize the GUI with the selected model
    chat_gui = gui.ChatGUI(models[args.model][0])

    # Initialize the local GPT4All model
    chat_model = model.ChatModel_gpt4all(model_path='./models', model_name=models[args.model][1])

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
    # Initialize the GUI with OpenAI model
    chat_gui = gui.ChatGUI('gpt 3.5-turbo')

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
    parser = argparse.ArgumentParser()

    # Define command-line arguments
    parser.add_argument('-a-', '--api', default=False, action='store_true',
                        help='Use this flag to run with the OpenAI API model.')
    parser.add_argument("-m", '--model', type=int, default=1, choices=[1, 2],
                        help="Choose a model number for the local GPT4All model.")

    # Parse arguments
    arguments = parser.parse_args()

    # Run the appropriate main function based on the arguments
    if arguments.api:
        main_api(arguments)
    else:
        main_local(arguments)
