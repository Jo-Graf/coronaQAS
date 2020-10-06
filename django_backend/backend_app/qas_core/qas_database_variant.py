from abc import ABC, abstractmethod
from typing import List, Union, Optional

from backend_app.qas_core.qas_document import QASDocument


class QASDatabaseVariant(ABC):
    def __init__(self):
        pass

    # TODO: add input to uml
    @abstractmethod
    def get_data(self, identifiers: Optional[Union[str, List[str]]] = None) -> List[QASDocument]:
        pass

    @abstractmethod
    def add_data(self, data: List[QASDocument]):
        pass