from typing import Optional, Dict, Any
from uuid import uuid4

import numpy as np
from haystack.database.base import Document


class QASDocument(Document):
    def __init__(self, text: str,
                 id: str = None,
                 query_score: Optional[float] = None,
                 question: Optional[str] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 embedding: Optional[np.array] = None):
        if id:
            id = str(id)
        else:
            id = str(uuid4())

        super().__init__(text=text,
                         id=id,
                         query_score=query_score,
                         question=question,
                         meta=meta,
                         embedding=embedding)
