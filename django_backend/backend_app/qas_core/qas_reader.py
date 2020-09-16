from typing import List

from backend_app.qas_core.qas_answer import QASAnswer
from backend_app.qas_core.qas_document import QASDocument


class QASReader:
    def __init__(self, variant=None):
        self.__variant = variant

    def set_variant(self, variant):
        self.__variant = variant

    def initialize(self):
        pass

    def read(self, query: str, data: List[QASDocument]) -> List[QASAnswer]:
        return self.__variant(query, data)