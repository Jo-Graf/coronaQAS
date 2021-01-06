from typing import List, Optional

from backend_app.qas_core.qas_answer import QASAnswer
from backend_app.qas_core.qas_document import QASDocument
from backend_app.qas_core.qas_reader_variant import QASReaderVariant


class QASReader:
    def __init__(self, variant: Optional[QASReaderVariant] = None):
        self.__variant = variant

    def set_variant(self, variant: QASReaderVariant):
        self.__variant = variant

    def initialize(self):
        pass

    def read(self, query: str, data: List[QASDocument]) -> List[QASAnswer]:
        return self.__variant.read(query, data)
