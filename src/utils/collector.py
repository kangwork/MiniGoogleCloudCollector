from utils.logger import get_sub_file_logger

class Collector:
    """
    A class to represent a Collector

    Attributes:
    - logger: Logger, the logger
    """
    def __init__(self, collector_name: str):
        self.logger = get_sub_file_logger(collector_name)
        
    def collect_resources(self):
        """
        Collect all resources in the project
        """
        raise NotImplementedError

    def collect_resource(self, *args):
        """
        Collect a specific resource with the given arguments
        """
        raise NotImplementedError