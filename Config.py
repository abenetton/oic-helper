import json

class Host:
    def __init__(self, label: str, base_url: str, token: str):
        self.label = label
        self.base_url = base_url
        self.token = token

    def __repr__(self):
        return f"Host(label={self.label}, base_url={self.base_url}, token=****)"

class Config:
    def __init__(self, hosts: dict[str, Host] = None, packages: list[str] = None):
        self.hosts: dict[str, Host] = hosts
        self.packages: list[str] = packages

    @classmethod
    def from_dict(cls, data):
        return cls(
            hosts=data.get("hosts", {}),
            packages=data.get("packages", [])
        )

    def load_from_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.hosts = {key: Host(**value) for key, value in data.get("hosts", {}).items()}
        self.packages = data.get("packages", [])

    def __repr__(self):
        return f"Config(hosts={list(self.hosts.keys())}, packages={self.packages})"

if __name__ == "__main__":
    # Example usage
    config = Config()
    config.load_from_file('data/config.json')
    print(config.hosts)