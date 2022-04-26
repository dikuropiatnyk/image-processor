from dotenv import dotenv_values

from utils.constants import SECRETS_FILENAME


class SecretsHolder:
    def __init__(self):
        self._journal = {}

    def __getattr__(self, item):
        return self._journal[item]

    def download(self):
        """
        Loads all needed data from the environment file
        """
        for key, value in dotenv_values(SECRETS_FILENAME).items():
            self._journal[key] = value
