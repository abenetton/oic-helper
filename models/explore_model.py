from models.config import Config
from oic_tools.OICHost import OICHost


class ExploreModel:
    def __init__(self):
        self.hosts = {}
        self.config = Config()

    def fetch_hosts(self) -> dict[str, OICHost]:
        # Load hosts from the configuration
        self.hosts = self.config.hosts
        return self.hosts
