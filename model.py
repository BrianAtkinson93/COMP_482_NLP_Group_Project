import openai


class ChatModel:
    def __init__(self, api_key):
        """

        :param api_key:
        """
        openai.api_key = api_key
        self.messages = []

    def send_message(self, user_message):
        """

        :param user_message:
        :return:
        """
        self.messages.append({"role": "user", "content": user_message})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
            chat_message = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": chat_message})
            return chat_message
        except Exception as e:
            return f"Error: {e}"
