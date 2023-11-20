import configparser

class Config:
    def __init__(self, filename='data/config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.api_key = self.config['openai']['api_key']

config = Config()
