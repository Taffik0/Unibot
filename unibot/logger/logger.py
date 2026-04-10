from datetime import datetime

RESET: str = "\033[0m"


class Logger():
    def __init__(self, info_color: str = "\033[1;32m"):
        self.info_color = info_color

    def info(self, msg: str):
        print(f"{datetime.now()} {self.info_color}[INFO]{RESET} {msg}")


_logger: Logger | None = None


def logger() -> Logger:
    global _logger
    if _logger is not None:
        return _logger
    _logger = Logger()
    return _logger
