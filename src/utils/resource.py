# Abstract Class for All Resources
class Resource:
    def __init__(self, resource: dict):
        """
        Initialize the resource
        """
        self._resource = resource
        return

    def __repr__(self) -> str:
        """
        Convert the resource to a string
        i.e., return all the attributes of the resource as a dictionary and then convert it to the string
        """
        return str(self._resource)
