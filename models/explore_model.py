from typing import List
from oic_tools.OICHost import OICHost

class ExploreModel:
    def __init__(self):
        self.data = []
        self.hosts = []

    def fetch_data(self):
        # Example method to fetch data
        self.data = ["Item 1", "Item 2", "Item 3"]

    def fetch_hosts(self) -> List[OICHost]:
        # Example: Mock data for OICHost objects
        self.hosts = [
            OICHost("SVIL", "SVILUPPO", "baseurl", "token", 
                [
                    "Boscolo.Services.SRM.Contracts",
                    "Boscolo.Services.SRM.Dashboard",
                    "Boscolo.Services.SRM.Notifications",
                    "Boscolo.Services.SRM.Sourcing",
                    "Boscolo.Services.SRM.Tenders"
                ]
            ),
            OICHost("PROD", "PRODUZIONE", "baseurl", "token", 
                [
                    "Boscolo.Services.SRM.Contracts",
                    "Boscolo.Services.SRM.Dashboard",
                    "Boscolo.Services.SRM.Tenders"
                ]
            ),
        ]
        return self.hosts
