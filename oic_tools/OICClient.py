from httpx import Client

import Config
from oic_tools.OICPackage import OICPackage


class OICClient:
    """
    A class to represent an OIC client.
    """

    def __init__(self, host: Config.Host):
        """
        Initializes the OICClient.

        :param host: Host object.
        """
        self.host = host
        self.client = Client(base_url=host.base_url, headers={"Authorization": f"Basic {host.token}"})

    def __repr__(self):
        return f"OICClient(host={self.host.label})"

    def get_all_packages(self):
        """
        Fetches all packages from the OIC server.

        :return: List of packages.
        """
        response = self.client.get("/ic/api/integration/v1/packages")
        if response.status_code == 200:
            resp_obj = response.json()
            return [OICPackage(package.get("id"), package.get("name"), package.get("countOfIntegrations")) for package
                    in resp_obj.get("items", [])]
        else:
            raise Exception(f"Failed to fetch packages: {response.status_code} - {response.text}")
