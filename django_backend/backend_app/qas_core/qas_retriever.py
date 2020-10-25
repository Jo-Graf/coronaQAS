from typing import Optional, Dict, Any, List

from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_doc_type_enum import QASDocType
from backend_app.qas_core.qas_document import QASDocument
from backend_app.qas_core.qas_retriever_variant import QASRetrieverVariant


class QASRetriever:
    def __init__(self, variant: Optional[QASRetrieverVariant] = None):
        self.__variant = variant

    def set_variant(self,  variant: QASRetrieverVariant):
        self.__variant = variant

    def initialize(self):
        pass

    # TODO: add param and return type to uml
    def retrieve(self, query: str, database: QASDatabase, doc_type: Optional[QASDocType] = None) -> List[QASDocument]:
        return self.__variant.retrieve(query, database, doc_type)
