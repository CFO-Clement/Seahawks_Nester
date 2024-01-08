import logging
import threading

from colorama import init, Fore, Style

init(autoreset=True)


class Log:
    def __init__(self, name="my_logger", log_file=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] (%(threadName)s) - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self.lock = threading.Lock()

    def log(self, level, message):
        with self.lock:
            if level == "debug":
                self.logger.debug(Fore.CYAN + Style.BRIGHT + message)
            elif level == "info":
                self.logger.info(Fore.GREEN + Style.BRIGHT + message)
            elif level == "warning":
                self.logger.warning(Fore.YELLOW + Style.BRIGHT + message)
            elif level == "error":
                self.logger.error(Fore.RED + Style.BRIGHT + message)
            elif level == "critical":
                self.logger.critical(Fore.RED + Style.BRIGHT + message)

    def debug(self, message):
        self.log("debug", message)

    def info(self, message):
        self.log("info", message)

    def warning(self, message):
        self.log("warning", message)

    def error(self, message):
        self.log("error", message)

    def critical(self, message):
        self.log("critical", message)
