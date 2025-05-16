import json
from typing import List
from oic_tools.OICHost import OICHost

class Config:
    CONFIG_FILE = "config.json"

    def __init__(self):
        self.hosts: dict[str, OICHost] = {}
        self.load()

    def load(self):
        """Load configuration from the JSON file."""
        try:
            with open(self.CONFIG_FILE, "r") as file:
                data = json.load(file)
                self.hosts = {
                    host["id"]: OICHost(
                        id=host["id"],
                        label=host["label"],
                        base_url=host["base_url"],
                        token=host["token"],
                        priority_package_ids=host.get("priority_package_ids", [])
                    )
                    for host in data.get("hosts", [])
                }
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")

    def save(self):
        """Save the current configuration to the JSON file."""
        data = {
            "hosts": [
                {
                    "id": host.id,
                    "label": host.label,
                    "base_url": host.base_url,
                    "token": host.token,
                    "priority_package_ids": host.priority_package_ids
                }
                for host in self.hosts.values()
            ]
        }
        try:
            with open(self.CONFIG_FILE, "w") as file:
                json.dump(data, file, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
