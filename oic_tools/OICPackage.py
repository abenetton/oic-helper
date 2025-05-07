from oic_tools.OICIntegration import OICIntegration


class OICPackage:
    """
    A class to represent an OIC package.
    """

    def __init__(self, id: str, name: str = "", integration_num: int = 0):
        self.id = id
        self.name = name if name else id
        self.integration_num = integration_num if integration_num > 0 else 0
        self.integration_list: list[OICIntegration] = []

    def __str__(self):
        return f"Package ID: {self.id}, Name: {self.name}, Integration Number: {self.integration_num}"
