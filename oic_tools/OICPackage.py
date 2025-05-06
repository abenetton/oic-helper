from oic_tools.OICIntegration import OICIntegration


class OICPackage:
    """
    A class to represent an OIC package.
    """

    def __init__(self, pid: str, name: str, integration_num: int):
        self.pid = pid
        self.name = name
        self.integration_num = integration_num
        self.integration_list: list[OICIntegration] = []

    def __str__(self):
        return f"Package ID: {self.pid}, Name: {self.name}, Integration Number: {self.integration_num}"
