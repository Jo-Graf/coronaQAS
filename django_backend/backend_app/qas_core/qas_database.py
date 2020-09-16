from typing import Optional, Dict, Any, List
from backend_app.qas_core.qas_data_loader import QASDataLoader
from backend_app.qas_core.qas_database_variant import QASDatabaseVariant
from backend_app.qas_core.qas_document import QASDocument


class QASDatabase:

    def __init__(self, variant: Optional[QASDatabaseVariant] = None, loader: Optional[QASDataLoader] = None):
        self.__variant = variant
        self.__data = []
        self.__loader = loader

    def set_variant(self, variant: QASDatabaseVariant):
        self.__variant = variant

    def get_variant(self) -> Optional[QASDatabaseVariant]:
        return self.__variant

    def set_loader(self, loader: QASDataLoader):
        self.__loader = loader

    def get_data(self) -> List[QASDocument]:
        return self.__variant.get_data()

    def load_data(self):
        new_data = self.__loader.load_data()
        self.add_data(new_data)

    def add_data(self, data: List[QASDocument]):
        self.__variant.add_data(data)
        self.__data.append(data)
