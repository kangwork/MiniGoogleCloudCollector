import logging

logfile = "../mnt/logs/log.log"


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
        self._formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self._file_handler = None
        self._stream_handler = None
        return

    def set_file_handler(self, log_file: str):
        # File Handler(For File Output)
        with open(log_file, "a") as f:
            f.write("")
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


def _setup_logger(logger: Logger, to_file: bool) -> None:
    """
    Ask a user if they want to log the output in a file or on the console
    """
    if to_file:
        logger.set_file_handler(logfile)

    else:
        logger.set_stream_handler()

    return


def get_sub_file_logger(module_name: str = __name__) -> Logger:
    """
    Get a logger for the sub files
    """
    logger = Logger(module_name)
    _setup_logger(logger, to_file=True)
    if module_name == "__main__":
        with open(logfile, "w") as f:
            f.write("")
            logger.add_info("Starting the main program.")
    return logger


def get_console_logger(module_name: str = __name__) -> Logger:
    """
    Get a logger for the console
    """
    logger = Logger(module_name)
    _setup_logger(logger, to_file=False)
    return logger
