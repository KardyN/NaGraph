import logging


class Logger(logging.Logger):
    def __init__(self, name: str, level: int = logging.DEBUG):
        super().__init__(name=name, level=level)


logging.setLoggerClass(Logger)
logger: Logger = logging.getLogger(__name__)
