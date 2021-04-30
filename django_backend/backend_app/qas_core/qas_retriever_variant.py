from abc import ABC, abstractmethod
from typing import List, Optional
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_doc_type_enum import QASDocType
from backend_app.qas_core.qas_document import QASDocument


class QASRetrieverVariant(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(self,
                 query: str,
                 database: QASDatabase,
                 doc_type: Optional[QASDocType] = None,
                 load_doc_meta: Optional[bool] = False) -> List[QASDocument]:
        pass
