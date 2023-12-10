import openai
from gpt4all import GPT4All


class ChatModel_gpt4all:
    """
    A class to handle interactions with a local GPT4All model.

    Attributes:
        path (str): The path to the directory containing the model.
        name (str): The name of the model file.
        model (GPT4All): An instance of the GPT4All model.
    """
    def __init__(self, model_path, model_name):
        """
        Initializes the ChatModel_gpt4all with the specified model.

        Args:
            model_path (str): The path to the directory containing the model.
            model_name (str): The name of the model file.
        """
        self.path = model_path
        self.name = model_name
        self.model = GPT4All(model_path=self.path, model_name=self.name, allow_download=False)

    def send_message(self, user_message):
        """
        Sends a message to the GPT4All model and returns its response.

        Args:
            user_message (str): The message from the user to be sent to the model.

        Returns:
            str: The response from the model.
        """ 
        with self.model.chat_session():
            output = self.model.generate(user_message, max_tokens=500)
        return output


class ChatModel_open_ai:
    """
    A class to handle interactions with the OpenAI API model.

    Attributes:
        messages (list): A list to store the conversation history.
    """
    def __init__(self, api_key):
        """
        Initializes the ChatModel_open_ai with the provided API key.

        Args:
            api_key (str): The API key for accessing OpenAI's GPT model.
        """
        openai.api_key = api_key
        self.messages = []

    def send_message(self, user_message):
        """
        Sends a message to the OpenAI API model and returns its response.

        Args:
            user_message (str): The message from the user to be sent to the model.

        Returns:
            str: The response from the model, or an error message if an exception occurs.
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
