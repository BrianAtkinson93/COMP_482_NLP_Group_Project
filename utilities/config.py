import configparser


class Config:
    """
    A class to manage configuration settings for the application.

    This class reads configuration settings from a specified INI file and provides
    an interface to access these settings throughout the application.

    Attributes:
        config (configparser.ConfigParser): An instance of ConfigParser to read and parse the INI file.
        api_key (str): The API key for OpenAI, read from the configuration file.
    """
    def __init__(self, filename='data/config.ini'):
        """
        Initializes the Config object by reading the specified INI file.

        Args:
            filename (str): The path to the configuration INI file. Defaults to 'data/config.ini'.
        """
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.api_key = self.config['openai']['api_key']


config = Config()
