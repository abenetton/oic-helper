from typing import List, Tuple

import datetime
import os
from models.compare_model import CompareModel
from oic_tools import OICHost, OICIntegration


def filter_compare_results(compare_results: List[Tuple[str, List[OICIntegration.OICCompare]]]) -> List[
    Tuple[str, List[OICIntegration.OICCompare]]]:
    res: List[Tuple[str, List[OICIntegration.OICCompare]]] = []

    for elem in compare_results:
        tmp: List[OICIntegration.OICCompare] = [x for x in elem[1] if
                                                x.result != OICIntegration.OICCompare.CompareResultEnum.EQUAL]
        if tmp:
            res.append((elem[0], sorted(tmp, key=lambda x: x.result.name)))

    return res

class CompareController:
    def __init__(self, model: CompareModel, view):
        self.compare_res = None
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

    def compare_hosts(self, host1: OICHost, host2: OICHost):
        # Logic to compare the two hosts
        self.host1_id = host1.id
        self.host2_id = host2.id
        self.compare_res = host1.compare(host2)
        self.view.update_package_tree(filter_compare_results(self.compare_res))

    def generate_report(self):
        # Logic to generate a report based on the comparison results
        if self.compare_res:
            # Generate the report using the comparison results and write it to a file

            # Create a directory for the report if it doesn't exist
            report_dir = "report"
            os.makedirs(report_dir, exist_ok=True)

            # Generate the report filename and path
            report_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}_report.md"
            report_path = os.path.join(report_dir, report_filename)

            # Load hosts
            host1: OICHost = self.model.fetch_hosts()[self.host1_id]
            host2: OICHost = self.model.fetch_hosts()[self.host2_id]

            # Write the report content to the file
            with open(report_path, "w") as report_file:
                report_file.write("# Host Comparison Report\n")
                report_file.write(f"- Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                report_file.write(f"- Host 1: {host1.label} ({host1.id})\n")
                report_file.write(f"- Host 2: {host2.label} ({host2.id})\n")
                for package_name, integrations in filter_compare_results(self.compare_res):
                    report_file.write(f"## Package: {package_name}\n")
                    for integration in integrations:
                        report_file.write(f"- Integration: {integration.name}\n")
                        report_file.write(f"\t- Host1 Version: {integration.host1_version[0]} - {integration.host1_version[1]}\n")
                        if integration.host2_version:
                            report_file.write(f"\t- Host2 Version: {integration.host2_version[0]} - {integration.host2_version[1]}\n")
                        else:
                            report_file.write("\t- Host2 Version: N/A\n")
                        report_file.write(f"\t- Result: {integration.result.value}\n")
        else:
            raise ValueError("No comparison results available. Please compare hosts first.")