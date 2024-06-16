import inspect
import logging
import sys


class Logger:
    """
    Logger singleton class.
    """

    __instances = {}

    def __new__(cls, filename=None):
        if filename is None:
            filename = inspect.getmodule(inspect.stack()[1][0]).__name__
        if filename not in cls.__instances:
            instance = super().__new__(cls)
            instance.filename = filename
            instance.logger = logging.getLogger(filename)
            instance.logger.setLevel(logging.INFO)
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            stream_handler.setFormatter(formatter)
            instance.logger.addHandler(stream_handler)
            cls.__instances[filename] = instance
        return cls.__instances[filename]

    def log_info(self, msg: str):
        self.logger.info(msg)

    def log_exception(self, msg: str):
        self.logger.exception(msg)

    def log_warning(self, msg: str):
        self.logger.warning(msg)

    def log_error(self, msg: str):
        self.logger.error(msg)