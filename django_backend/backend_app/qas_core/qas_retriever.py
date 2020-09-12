from typing import Optional, Dict, Any, List

from backend_app.qas_core.qas_retriever_variant import QASRetrieverVariant


class QASRetriever:
    def __init__(self, variant: Optional[QASRetrieverVariant] = None):
        self.__variant = variant

    def set_variant(self,  variant: QASRetrieverVariant):
        self.__variant = variant

    def initialize(self):
        pass

    def retrieve(self):
        self.__variant.retrieve()
