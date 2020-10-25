from typing import Optional, Dict, Any
from uuid import uuid4

import numpy as np
from haystack import Document


class QASDocument(Document):

    # TODO: add changes in input params (probability=probability) to uml
    def __init__(self, text: str,
                 id: str = None,
                 query_score: Optional[float] = None,
                 question: Optional[str] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 embedding: Optional[np.array] = None,
                 probability: Optional[float] = None):

        if id:
            identifier = str(id)
        else:
            identifier = str(uuid4())

        super().__init__(text=str(text),
                         id=identifier,
                         score=query_score,
                         question=question,
                         meta=meta,
                         embedding=embedding,
                         probability=probability)

    @staticmethod
    def doc_to_qas_doc(document: Document):
        return QASDocument(text=document.text,
                           id=document.id,
                           query_score=document.score,
                           question=document.question,
                           meta=document.meta,
                           probability=document.probability)

    def to_dict(self, field_map={}):
        inv_field_map = {v: k for k, v in field_map.items()}
        _doc: Dict[str, str] = {}
        for k, v in self.__dict__.items():
            k = k if k not in inv_field_map else inv_field_map[k]
            _doc[k] = v
        return _doc
