from database.db import Home
from dataclasses import dataclass

@dataclass
class Config:
    timeout: int

    @staticmethod
    def default():
        return Config(
            timeout=60
        )


class ConfigRepository:
    def __init__(self):
        self.config = None
        self.load()

    def load(self):
        try:
            home = Home.get_active()

            return Config(
                timeout=home.timeout if home else 60
            )
        except Exception as e:
            self.config = Config.default()

    def get(self):
        """

        :return: Config
        """
        return self.config or Config.default()