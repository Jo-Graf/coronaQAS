from typing import List, Optional

from backend_app.qas_core.qas_data_loader_variant import QASDataLoaderVariant
from backend_app.qas_core.qas_document import QASDocument


class QASDataLoader:

    def __init__(self, source_path: str = '', output_path: str = '', variant: Optional[QASDataLoaderVariant] = None):
        self.__variant = variant
        self.__data = None
        self.source_path = source_path
        self.output_path = output_path
        self.data_is_loaded = False

    def set_variant(self, variant):
        self.__variant = variant

    def data_is_loaded(self) -> bool:
        return self.data_is_loaded

    def load_data(self) -> List[QASDocument]:
        self.data_is_loaded, self.__data = self.__variant.load_data()
        return self.data_is_loaded, self.__data

    def get_doc_base_key(self, doc: Optional[QASDocument] = None, key: Optional[str] = None) -> str:
        return self.__variant.get_doc_base_key(doc, key)
