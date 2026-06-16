import logging
import os
from datetime import datetime

def get_logger(logger_name="automation_logger"):
    """Configure and return a logger instance."""

    # Create a logs folder inside reports/
    logs_dir = os.path.join("reports", "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Log file with timestamp
    log_file = os.path.join(logs_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # Create a custom logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate logs
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Log format
        formatter = logging.Formatter(
            fmt="%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Attach formatters
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
