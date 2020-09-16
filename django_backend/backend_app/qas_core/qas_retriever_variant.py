from abc import ABC, abstractmethod
from typing import List
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_document import QASDocument


class QASRetrieverVariant(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(self, query: str, database: QASDatabase) -> List[QASDocument]:
        pass
