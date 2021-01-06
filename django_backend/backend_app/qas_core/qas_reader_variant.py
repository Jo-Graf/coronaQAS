from abc import ABC, abstractmethod
from typing import List

from backend_app.qas_core.qas_answer import QASAnswer
from backend_app.qas_core.qas_document import QASDocument


class QASReaderVariant(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def read(self, query: str, data: List[QASDocument]) -> List[QASAnswer]:
        pass


