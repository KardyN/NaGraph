import logging

from gcloud.access import CloudAccessor
from gui.app import App
from util.logger import Logger

log = logging.getLogger("nagraph")


def main():
    Logger()
    log.info("NaGraph started")
    app = App()
    app.mainloop()
    log.info("NaGraph closed")


if __name__ == "__main__":
    main()
