import json

from oic_tools.OICHost import OICHost


class Config:
    def __init__(self, hosts: dict[str, OICHost] = None, packages: list[str] = None):
        self.hosts: dict[str, OICHost] = hosts

    @classmethod
    def from_dict(cls, data):
        return cls(
            hosts=data.get("hosts", {})
        )

    def load_from_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.hosts = {host.get("id", ""): OICHost(**host) for host in data.get("hosts", [])}

    def __repr__(self):
        return f"Config(hosts={list(self.hosts.keys())})"

if __name__ == "__main__":
    # Example usage
    config = Config()
    config.load_from_file('data/config.json')
    print(config.hosts)