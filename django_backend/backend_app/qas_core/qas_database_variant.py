from abc import ABC, abstractmethod
from typing import List

from backend_app.qas_core.qas_document import QASDocument


class QASDatabaseVariant(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_data(self) -> List[QASDocument]:
        pass

    @abstractmethod
    def add_data(self, data: List[QASDocument]):
        pass