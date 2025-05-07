from typing import List, Tuple


class OICIntegration:
    """
    This class is responsible for integrating with the OIC (Oracle Integration Cloud) system.
    It handles the connection to the OIC, sending requests, and processing responses.
    """

    def __init__(self, id: str, code: str, name: str, status: str, version: str):
        self.id = id
        self.code = code
        self.name = name
        self.versions: List[Tuple[str, str]] = [(version, status)]

    def add_version(self, version: str, status: str) -> None:
        """
        Adds a new version to the integration.

        :param version: The version of the integration.
        :param status: The status of the integration.
        """
        self.versions.append((version, status))
        self.versions = sorted(self.versions, key=lambda x: x[0], reverse=True)
