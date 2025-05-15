from models.config import Config
from oic_tools.OICHost import OICHost


class CompareModel:
    def __init__(self):
        self.hosts = {}
        self.config = Config()

    def fetch_hosts(self) -> dict[str, OICHost]:
        if not self.hosts:
            # Load hosts from the configuration
            self.hosts = self.config.hosts
        return self.hosts
