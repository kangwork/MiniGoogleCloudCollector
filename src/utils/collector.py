from utils.logging import get_sub_file_logger
from google.oauth2.service_account import Credentials


class Collector:
    """
    A class to represent a Collector

    Attributes:
    - logger: Logger, the logger
    - credentials: Credentials, the credentials
    - project_id: str, the project ID
    """
    def __init__(self, collector_name: str, credentials: Credentials=None):
        self.logger = get_sub_file_logger(collector_name)
        if credentials and isinstance(credentials, Credentials):
            self.credentials = credentials
            self.project_id = credentials.project_id
        else:
            self.credentials = None
            self.project_id = None

    def get_route_messages(self, route_messages: dict[str, (str, str)]) -> str:
        """
        Get the route messages

        :param dict[str, (str, str)]: the route messages
            - key: str, the route
            - value: (str, str), the route description and example

        :return: str, the route messages
        """
        if not route_messages:
            raise NotImplementedError("The route_messages should be provided from the child collector class.")
        messages = "\n"
        for route, (description, example) in route_messages.items():
            messages += f"{route}\n{description}\n(Example: {example})\n"
        return messages

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