import argparse

import gui
import model
import config


def main_local(args):
    models = {
        1: ("nous_hermes", "nous-hermes-llama2-13b.Q4_0.gguf"),
        2: ("mistral", "mistral-7b-openorca.Q4_0.gguf")
    }
    chat_gui = gui.ChatGUI(models[args.model][1])

    # Initialize model with the correct path and model name
    chat_model = model.ChatModel_gpt4all(model_path='./models', model_name=models[args.model][1])

    def send_message_wrapper():
        user_message = chat_gui.get_user_input()
        if user_message:
            response = chat_model.send_message(user_message)
            chat_gui.update_chat_history(f"User: {user_message}\n", 'user')
            chat_gui.update_chat_history(f"Bot: {response}\n", 'bot')

    chat_gui.set_send_message_action(send_message_wrapper)
    chat_gui.run()


def main_api(args):
    chat_gui = gui.ChatGUI('gpt 3.5-turbo')
    chat_model = model.ChatModel_open_ai(config.config.api_key)  # Note the change here

    def send_message_wrapper():
        user_message = chat_gui.get_user_input()
        if user_message:
            # Display user's question in the chat history
            chat_gui.update_chat_history(f"User: {user_message}\n", 'user')

            # Get and display the bot's response
            response = chat_model.send_message(user_message)
            chat_gui.update_chat_history(f"Bot: {response}\n", 'bot')

    chat_gui.set_send_message_action(send_message_wrapper)
    chat_gui.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Main arguments
    parser.add_argument('-a-', '--api', default=False, action='store_true',
                        help='If you would like to use api based gpt4 - set flag')
    parser.add_argument("-m", '--model', default=1, choices=[1, 2],
                        help="To use a different model, chose a number 1 - 2")

    arguments = parser.parse_args()

    if arguments.api:
        main_api(arguments)
    else:
        main_local(arguments)
