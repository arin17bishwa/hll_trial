import logging

def setup_logger(log_file="00.log"):
    # Create a logger
    logger = logging.getLogger("SimpleLogger")
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Define log format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    return logger
