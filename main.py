import gui
import model
import config


def main():
    chat_gui = gui.ChatGUI()
    chat_model = model.ChatModel(config.config.api_key)  # Note the change here

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
    main()
