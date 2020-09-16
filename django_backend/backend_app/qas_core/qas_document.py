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
            identifier = str(id)
        else:
            identifier = str(uuid4())

        super().__init__(text=str(text),
                         id=identifier,
                         query_score=query_score,
                         question=question,
                         meta=meta,
                         embedding=embedding)

    @staticmethod
    def doc_to_qas_doc(document: Document):
        return QASDocument(text=document.text,
                           id=document.id,
                           query_score=document.query_score,
                           question=document.question,
                           meta=document.meta)

    def to_dict(self, field_map={}):
        inv_field_map = {v: k for k, v in field_map.items()}
        _doc: Dict[str, str] = {}
        for k, v in self.__dict__.items():
            k = k if k not in inv_field_map else inv_field_map[k]
            _doc[k] = v
        return _doc