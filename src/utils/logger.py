import logging
import os
import sys
from logging.handlers import RotatingFileHandler

class ColorFormatter(logging.Formatter):
    """Custom formatter to add colors to console logs."""
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[34;20m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s [%(levelname)s] %(message)s"

    LEVEL_COLORS = {
        logging.DEBUG: grey,
        logging.INFO: blue,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red
    }

    def format(self, record):
        log_color = self.LEVEL_COLORS.get(record.levelno, self.reset)
        formatter = logging.Formatter(f"{log_color}{self.format_str}{self.reset}", datefmt='%H:%M:%S')
        return formatter.format(record)

def setup_logger(name: str = "webscraper", log_level: int = logging.INFO):
    """Sets up a professional logger with colored console and rotating file handlers."""
    
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(root_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    # Handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)

    file_path = os.path.join(log_dir, "scraper.log")
    file_handler = RotatingFileHandler(
        file_path, 
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s'
    ))
    logger.addHandler(file_handler)

    return logger

# Create a default logger instance
logger = setup_logger()
