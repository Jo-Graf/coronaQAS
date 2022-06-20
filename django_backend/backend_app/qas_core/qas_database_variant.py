from abc import ABC, abstractmethod
from typing import List, Union, Optional, Dict

from backend_app.qas_core.qas_document import QASDocument


class QASDatabaseVariant(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_data(self,
                 identifiers: Optional[Union[str, List[str]]] = None,
                 query: Optional[Union[str, Dict]] = None
                 ) -> List[QASDocument]:
        pass

    @abstractmethod
    def add_data(self, data: List[QASDocument]):
        pass


