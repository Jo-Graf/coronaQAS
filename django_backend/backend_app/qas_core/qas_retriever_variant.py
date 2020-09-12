from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from backend_app.qas_core.qas_document import QASDocument


class QASRetrieverVariant(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(self) -> List[QASDocument]:
        pass
