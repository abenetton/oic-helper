from __future__ import annotations

from enum import Enum
from typing import List, Tuple
from loguru import logger

class OICIntegration:
    """
    This class is responsible for integrating with the OIC (Oracle Integration Cloud) system.
    It handles the connection to the OIC, sending requests, and processing responses.
    """

    def __init__(self, id: str, code: str, name: str, status: str, version: str):
        self.id = id
        self.code = code
        self.name = name
        self.versions: List[Tuple[str, str]] = [(version, status)]

    def add_version(self, version: str, status: str) -> None:
        """
        Adds a new version to the integration.

        :param version: The version of the integration.
        :param status: The status of the integration.
        """
        self.versions.append((version, status))
        self.versions = sorted(self.versions, key=lambda x: x[0], reverse=True)


    def compare(self, other: OICIntegration | None) -> OICIntegration.OICCompare:
        """
        Compare two OICIntegration instances.

        :param other: Another OICIntegration instance.
        :return: True if they are the same, False otherwise.
        """
        if not other:
            logger.warning(f"OICIntegration {self.id} has no corresponding integration to compare with.")

        res = self.OICCompare(self.name, self.versions[0], other.versions[0] if other else None)
        return res

    class OICCompare:
        """
        This class is responsible for integrating with the OIC (Oracle Integration Cloud) system.
        It handles the connection to the OIC, sending requests, and processing responses.
        """

        class CompareResultEnum(Enum):
            EQUAL = "Versions are equal"
            NEWER = "Host1 version is newer"
            OLDER = "Host1 version is older"
            HOST1_INACTIVE = "Integration is inactive on Host1"
            HOST2_INACTIVE = "Integration is inactive on Host2"
            HOST2_MISSING = "Integration is missing on Host2"

        def __init__(self, name: str, host1_version: tuple[str, str], host2_version: tuple[str, str] | None):
            self.name = name
            self.host1_version = host1_version
            self.host2_version = host2_version
            self.result = self.compare_result(host1_version, host2_version) if host2_version else self.CompareResultEnum.HOST2_MISSING

        @classmethod
        def compare_result(cls, version1: tuple[str, str], version2: tuple[str, str]) -> CompareResultEnum:
            """
            Compare two versions and return a comparison value.

            :param version1: The first version to compare.
            :param version2: The second version to compare.
            :return: -1 if version1 < version2, 1 if version1 > version2, 0 if equal.
            """

            def parse_version(version: str) -> List[int]:
                return [int(part) for part in version.split(".")]

            v1_parts = parse_version(version1[0])
            v2_parts = parse_version(version2[0])

            if v1_parts > v2_parts:
                return cls.CompareResultEnum.NEWER
            elif v1_parts < v2_parts:
                return cls.CompareResultEnum.OLDER
            elif version1[1] == 'ACTIVATED' and version2[1] != 'ACTIVATED':
                return cls.CompareResultEnum.HOST2_INACTIVE
            elif version1[1] != 'ACTIVATED' and version2[1] == 'ACTIVATED':
                return cls.CompareResultEnum.HOST1_INACTIVE
            else:
                return cls.CompareResultEnum.EQUAL