from httpx import Client

from oic_tools.OICPackage import OICPackage


class OICHost:
    def __init__(self, id: str, label: str, base_url: str, token: str, priority_package_ids: list[str]):
        self.id = id
        self.label = label
        self.base_url = base_url
        self.token = token
        self.priority_package_ids = sorted(priority_package_ids)
        self.client = Client(base_url=self.base_url, headers={"Authorization": f"Basic {self.token}"})
        self.packages: dict[str, OICPackage] = {pkg_id: OICPackage(self.client, pkg_id) for pkg_id in priority_package_ids}
        self.packages_loaded = False

    def load_all_packages(self) -> None:
        """
        Fetches all packages from the OIC server.

        :return: List of packages.
        """
        response = self.client.get("/ic/api/integration/v1/packages")
        if response.status_code == 200:
            resp_obj = response.json()
            self.packages = {package.get("id"): OICPackage(self.client, package.get("id"), package.get("name"),
                                                           package.get("countOfIntegrations")) for package in
                             resp_obj.get("items", [])}
            self.packages_loaded = True
        else:
            self.packages_loaded = False
            raise Exception(f"Failed to fetch packages: {response.status_code} - {response.text}")

    def get_sorted_package_ids(self, priority_packages_sort: bool = False) -> list[str]:
        """Return a sorted list of packages, optionally prioritizing favorites."""
        package_ids = self.packages.keys()

        if priority_packages_sort:
            # Split packages into two lists, one for those with name in config and one for those not
            packages_priority = [pkg for pkg in package_ids if pkg in self.priority_package_ids]
            packages_not_priority = [pkg for pkg in package_ids if pkg not in self.priority_package_ids]

            # Join the two lists keeping the packages in config first and sorting individual lists by name
            return sorted(packages_priority) + sorted(packages_not_priority)
        else:
            return sorted(package_ids)

    def __repr__(self):
        return f"Host(label={self.label}, base_url={self.base_url}, token=****)"
