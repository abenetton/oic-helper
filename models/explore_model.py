from typing import List
from oic_tools.OICHost import OICHost
from models.config import Config

class ExploreModel:
    def __init__(self):
        self.data = []
        self.hosts = []
        self.config = Config()

    def fetch_hosts(self) -> List[OICHost]:
        # Load hosts from the configuration
        self.hosts = self.config.hosts
        return self.hosts
