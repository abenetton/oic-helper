from models.compare_model import CompareModel
from oic_tools import OICHost


class CompareController:
    def __init__(self, model: CompareModel, view):
        self.model = model
        self.view = view
        self.host1_id = ""
        self.host2_id = ""

        hosts: list[OICHost] = [x for x in self.model.fetch_hosts().values()]
        self.view.update_host_list(True, hosts)
        self.update_host2(hosts[0])

    def update_host2(self, host1: OICHost):
        host2_list = [x for x in self.model.fetch_hosts().values() if x.id != host1.id]
        # Logic to update the second host based on the first host selection
        # This could involve filtering or updating the available options in the view
        self.view.update_host_list(False, host2_list)