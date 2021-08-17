import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_PATH = os.getenv("LOG_PATH")

# Utility class that provides rolling logs
class LogFactory():
    @staticmethod
    def getLogger(__name__) -> logging.Logger:
        format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', '%m/%d/%Y %I:%M:%S %p')
        handler = TimedRotatingFileHandler(LOG_PATH,
                                        when="D",
                                        interval=1,
                                        backupCount=0,
                                        encoding='utf-8')
        handler.setFormatter(format)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger
