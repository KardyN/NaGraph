from pathlib import Path

from gui.app import App
from util.config import Config
from gcloud.access import CloudAccessor
from util.logger import Logger


def main():
    Logger(__name__)
    app = App()
    Config(Path(__name__).resolve().parent)
    CloudAccessor()
    app.mainloop()


if __name__ == "__main__":
    main()
