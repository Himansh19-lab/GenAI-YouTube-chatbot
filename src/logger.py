
from email.mime import message
import logging
import os


class Logger:
    def __init__(self, name: str, log_file: str = "app.log", level: str = "DEBUG"):
        self.dict_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        self.log_file = log_file
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.dict_levels.get(level, logging.DEBUG))
        self.setup()


    def setup(self):
        logs = "logs"
        os.makedirs(logs, exist_ok=True)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.dict_levels.get(self.logger.level, logging.DEBUG))

        file_handler = logging.FileHandler(os.path.join(logs, self.log_file), mode="w")
        file_handler.setLevel(self.dict_levels.get(self.logger.level, logging.DEBUG))

        formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s : %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)


    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    



