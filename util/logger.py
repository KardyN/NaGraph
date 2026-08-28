import logging


class Logger(logging.Logger):
    def __init__(self, name: str = __name__, level: int = logging.DEBUG):
        super().__init__(name=name, level=level)


logging.setLoggerClass(Logger)
log = logging.getLogger("nagraph")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("debug.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
log.addHandler(fh)
log.addHandler(ch)
