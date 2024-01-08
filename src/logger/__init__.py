# logger/__init__.py

"""
if __name__ == "__main__":
    logger = ThreadSafeLogger("example_logger", "example.log")
    logger.debug("Ceci est un message de débogage.")
    logger.info("Ceci est un message d'information.")
    logger.warning("Ceci est un message d'avertissement.")
    logger.error("Ceci est un message d'erreur.")
    logger.critical("Ceci est un message critique.")
"""

from .logger import Log
