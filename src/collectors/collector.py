from utils.logging import Logger, get_sub_file_logger
from google.oauth2.service_account import Credentials
from abc import ABC, abstractmethod


class Collector(ABC):
    """
    A class to represent a Collector

    Attributes:
    - logger: Logger, the logger
    - credentials: Credentials, the credentials
    - project_id: str, the project ID
    """

    logger: Logger
    credentials: Credentials
    project_id: str

    def __init__(self, collector_name: str, credentials: Credentials):
        self.logger = get_sub_file_logger(collector_name)
        self.credentials = credentials
        self.project_id = credentials.project_id

    @classmethod
    def get_route_messages(self, route_messages: dict[str, (str, str)]) -> str:
        """
        Get the route messages

        :param dict[str, (str, str)]: the route messages
            - key: str, the route
            - value: (str, str), the route description and example

        :return: str, the route messages
        """
        if not route_messages:
            raise NotImplementedError(
                "The route_messages should be provided from the child collector class."
            )
        messages = "\n"
        for route, (description, example) in route_messages.items():
            messages += f"{route}\n{description}\n(Example: {example})\n"
        return messages

    @abstractmethod
    def collect_resources(self):
        """
        Collect all resources in the project
        """
        pass

    @abstractmethod
    def collect_resource(self, *args):
        """
        Collect a specific resource with the given arguments
        """
        pass
