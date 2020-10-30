from typing import List
from haystack.reader.base import BaseReader

from backend_app.qas_core.qas_answer import QASAnswer
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_document import QASDocument
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_reader_variant import QASReaderVariant
from backend_app.qas_core.qas_retriever_variant import QASRetrieverVariant


class QASHaystackReaderAdapter(QASReaderVariant):

    def __init__(self, reader:  BaseReader = None):
        self.__reader = reader

    def read(self, query: str, data: List[QASDocument]) -> List[QASAnswer]:
        docs = self.__reader.predict(query, data)
        print(docs)
        qas_docs = []

        for raw_answer in docs['answers']:
            answer = QASAnswer(
                answer=raw_answer['answer'],
                question=docs['question'],
                query_score=raw_answer['score'],
                probability=raw_answer['probability'],
                context=raw_answer['context'],
                offset_start=raw_answer['offset_start'],
                offset_end=raw_answer['offset_end'],
                offset_start_in_doc=raw_answer['offset_start_in_doc'],
                offset_end_in_doc=raw_answer['offset_end_in_doc'],
                no_ans_gap=docs['no_ans_gap'],
                doc_id=raw_answer['document_id']
            )

            doc_list = list(filter(lambda x: x.id == raw_answer['document_id'], data))

            if len(doc_list) > 0:
                doc = doc_list[0]
                meta_dict = doc.meta
                meta_dict
                answer.meta = meta_dict

            qas_docs.append(answer)

        return qas_docs
