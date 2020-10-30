import hashlib
from typing import Optional, Any, Dict
from uuid import uuid4
import numpy as np
from backend_app.qas_core.qas_document import QASDocument


class QASAnswer(QASDocument):

    # TODO: add attributes to uml
    def __init__(self,
                 answer: str,
                 offset_start_in_doc: Optional[int] = None,
                 offset_end_in_doc: Optional[int] = None,
                 offset_start: Optional[int] = None,
                 offset_end: Optional[int] = None,
                 probability: Optional[float] = None,
                 text: Optional[str] = '',
                 answer_id: Optional[str] = None,
                 doc_id: Optional[str] = None,
                 id: Optional[str] = None,
                 query_score: Optional[float] = None,
                 question: Optional[str] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 embedding: Optional[np.array] = None,
                 context: Optional[str] = None,
                 no_ans_gap: Optional[float] = None):

        if answer_id:
            identifier = str(answer_id)
        else:
            unique_key_components = {
                'answer': answer,
                'offset_start_in_doc': offset_start_in_doc,
                'offset_end_in_doc': offset_end_in_doc,
                'context': context,
                'probability': probability,
                'query_score': query_score}

            identifier = self._generate_id(**unique_key_components)

        self.answer = answer
        self.offset_start_in_doc = offset_start_in_doc
        self.offset_end_in_doc = offset_end_in_doc
        self.offset_start = offset_start
        self.offset_end = offset_end
        self.context = context
        self.answer_id = identifier
        self.doc_id = doc_id
        self.no_ans_gap = no_ans_gap

        super().__init__(text=text,
                         id=id,
                         query_score=query_score,
                         question=question,
                         meta=meta,
                         embedding=embedding,
                         probability=probability)

    # TODO: add to uml
    @staticmethod
    def _generate_id(**kwargs) -> str:
        unique_key_components = ['answer', 'offset_start_in_doc', 'offset_end_in_doc', 'context', 'probability', 'query_score']
        unique_key = ''.join([str(kwargs[x]) for x in unique_key_components]).encode('utf-8')
        unique_hashed_key = hashlib.md5(unique_key).hexdigest()
        return unique_hashed_key

    # TODO: add to uml
    def serialize(self):
        return self.__dict__
