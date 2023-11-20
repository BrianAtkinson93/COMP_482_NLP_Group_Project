import openai
from gpt4all import GPT4All


class ChatModel_gpt4all:
    def __init__(self, model_path, model_name):
        self.path = model_path
        self.name = model_name
        self.model = GPT4All(model_path=self.path, model_name=self.name, allow_download=False)

    def send_message(self, user_message):
        with self.model.chat_session():
            output = self.model.generate(user_message, max_tokens=500)
        return output


class ChatModel_open_ai:
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
