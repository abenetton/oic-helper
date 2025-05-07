from httpx import Client

from oic_tools.OICIntegration import OICIntegration


class OICPackage:
    """
    A class to represent an OIC package.
    """

    def __init__(self, client: Client, id: str, name: str = "", integration_num: int = 0):
        self.id = id
        self.name = name if name else id
        self.integration_num = integration_num if integration_num > 0 else 0
        self.integrations_loaded = False
        self.integrations: dict[str, OICIntegration] = {}
        self.client = client

    def load_all_integrations(self) -> None:
        response = self.client.get(f"/ic/api/integration/v1/packages/{self.id}")
        if response.status_code == 200:
            resp_obj = response.json()

            # For each integration, either add it to the list or update the existing one with new versions
            for integration in resp_obj.get("integrations", []):
                integration_code = integration.get("code")

                if integration_code in self.integrations:
                    # Update existing integration with new version
                    self.integrations[integration_code].add_version(integration.get("version"), integration.get("status"))
                else:
                    # Create a new integration
                    self.integrations[integration_code] = OICIntegration(
                        integration.get("id"),
                        integration.get("code"),
                        integration.get("name"),
                        integration.get("status"),
                        integration.get("version")
                    )

            self.integrations_loaded = True
        else:
            self.integrations_loaded = False
            raise Exception(f"Failed to fetch packages: {response.status_code} - {response.text}")

    def get_all_integrations(self) -> dict[str, OICIntegration]:
        """
        Returns all integrations in the package.
        """
        if not self.integrations_loaded:
            self.load_all_integrations()
        return self.integrations

    def __str__(self):
        return f"Package ID: {self.id}, Name: {self.name}, Integration Number: {self.integration_num}"
