from datetime import datetime

RESET: str = "\033[0m"


class Logger():
    def __init__(self, info_color: str = "\033[1;32m",
                 warn_color: str = "\033[1;33m",
                 debug_color: str = "\033[1;34m",
                 error_color: str = "\033[1;31m"):
        self._info_color = info_color
        self._warn_color = warn_color
        self._debug_color = debug_color
        self._error_color = error_color

    def info(self, msg: str):
        print(f"{datetime.now()} {self._info_color}[INFO]{RESET} {msg}")

    def warn(self, msg: str):
        print(f"{datetime.now()} {self._warn_color}[WARN]{RESET} {msg}")

    def debug(self, msg: str):
        print(f"{datetime.now()} {self._debug_color}[DEBUG]{RESET} {msg}")

    def error(self, msg: str):
        print(f"{datetime.now()} {self._error_color}[ERROR]{RESET} {msg}")


_logger: Logger | None = None


def logger() -> Logger:
    global _logger
    if _logger is not None:
        return _logger
    _logger = Logger()
    return _logger
