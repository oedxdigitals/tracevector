from abc import ABC, abstractmethod


class BaseStorage(ABC):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def create_case(self, case_id: str):
        pass

    @abstractmethod
    def add_scan(self, case_id: str, scan_data: dict):
        pass

    @abstractmethod
    def get_case(self, case_id: str):
        pass
