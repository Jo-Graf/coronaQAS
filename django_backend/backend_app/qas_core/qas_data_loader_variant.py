from abc import ABC, abstractmethod
import abc
from typing import List, Optional

from backend_app.qas_core.qas_document import QASDocument


class QASDataLoaderVariant(ABC):

    def __init__(self, source_path: Optional[str] = None, output_path: Optional[str] = None):
        self._source_path = source_path
        self._output_path = output_path

    @abstractmethod
    def load_data(self) -> (bool, List[QASDocument]):
        pass

    @abstractmethod
    def get_doc_base_key(self, doc: Optional[QASDocument] = None, key: Optional[str] = None) -> str:
        pass