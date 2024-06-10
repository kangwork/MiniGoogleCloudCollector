import logging

# A class to log messages
class Logger:
    """
    A class to log messages

    Private Attributes
    ----------------
    - _logger: logging.Logger, the logger object
    - _file_handler: logging.FileHandler, the file handler
    - _stream_handler: logging.StreamHandler, the stream handler
    - _formatter: logging.Formatter, the formatter
    """
    def __init__(self, name: str = "MiniGoogleCloudCollector"):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._file_handler = None
        self._stream_handler = None
        return
    
    def set_file_handler(self, log_file: str):
        # File Handler(For File Output)
        self._file_handler = logging.FileHandler(log_file)
        self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)
        return
    
    def set_stream_handler(self):
        # Stream Handler(For Console Output)
        self._stream_handler = logging.StreamHandler()
        self._stream_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._stream_handler)
        return

    def add_info(self, message: str):
        self._logger.info(message)

    def add_error(self, message: str):
        self._logger.error(message)

    def add_warning(self, message: str):
        self._logger.warning(message)

    def add_debug(self, message: str):
        self._logger.debug(message)

    def add_critical(self, message: str):
        self._logger.critical(message)


def setup_logger(logger: Logger, to_file: bool) -> None:
    """
    Ask a user if they want to log the output in a file or on the console
    """
    if to_file:
        logger.set_file_handler("log.log")

    else:
        logger.set_stream_handler()
        
    return 


def setup_main_file_logger(logger: Logger) -> None:
    """
    Set up the logger for the main file
    """
    # Clear the log file
    with open("log.log", "w") as f:
        f.write("")
    setup_logger(logger, to_file=True)
    logger.add_info("Starting the main program.")
    return


def get_sub_file_logger(module_name: str = __name__) -> Logger:
    """
    Get the logger for the sub files
    """
    logger = Logger(module_name) # name of the caller? or name of this file? --> name of the caller
    # DO NOT clear the log file, but append to it
    setup_logger(logger, to_file=True)
    return logger


def get_console_logger(module_name: str = __name__) -> Logger:
    """
    Get the logger for the console
    """
    logger = Logger(module_name) # name of the caller? or name of this file? --> name of the caller
    setup_logger(logger, to_file=False)
    return logger