import logging

# A class to log messages
class Logger:
    """
    A class to log messages

    Private Attributes
    ----------------
    - _logger: logging.Logger, the logger object
    - _file_handler: logging.FileHandler, the file handler
    # - _stream_handler: logging.StreamHandler, the stream handler
    - _formatter: logging.Formatter, the formatter
    - _log_file: str, the log file path
    """
    def __init__(self, log_file: str | None = None):
        self._logger = logging.getLogger("MiniGoogleCloudCollector")
        self._logger.setLevel(logging.INFO)
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._log_file = log_file

        if log_file:
            # File Handler(For File Output)
            self._file_handler = logging.FileHandler(self._log_file)
            self._file_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._file_handler)
        else:
            # Stream Handler(For Console Output)
            self._stream_handler = logging.StreamHandler()
            self._stream_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._stream_handler)
        return


    def add_log(self, message: str):
        """
        Add a log message to the log, but do not format it(do not use any formatter).
        """
        self._logger.log(logging.INFO, message)

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

def setup_logger() -> Logger:
    """
    Ask a user if they want to log the output in a file or on the console
    """
    print("Do you want to log the output in a file? (y/n):")
    choice = input()
    if choice == 'y':
        logger = Logger("log.log")

        # Clear the log file (Overwrite)
        with open("log.log", "w") as f:
            f.write("")
    else:
        logger = Logger()
    logger.add_info("Starting the program.")
    return logger
    