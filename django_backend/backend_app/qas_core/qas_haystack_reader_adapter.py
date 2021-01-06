from typing import List
from haystack.reader.base import BaseReader

from backend_app.qas_core.qas_answer import QASAnswer
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_doc_key_gen import QASDocKeyGen
from backend_app.qas_core.qas_document import QASDocument
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_reader_variant import QASReaderVariant
from backend_app.qas_core.qas_retriever_variant import QASRetrieverVariant


class QASHaystackReaderAdapter(QASReaderVariant):

    def __init__(self, reader:  BaseReader = None):
        self.__reader = reader

    def read(self, query: str, data: List[QASDocument]) -> List[QASAnswer]:
        content_data = [x for x in data if x.meta['is_doc_meta'] is False]
        meta_data = [x for x in data if x.meta['is_doc_meta'] is True]

        docs = self.__reader.predict(query, content_data)
        qas_docs = []

        # Further answer processing
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

            meta_doc_list = list(filter(lambda x: x.id == QASDocKeyGen.get_doc_base_key(key=raw_answer['document_id']), meta_data))
            doc_list = list(filter(lambda x: x.id == raw_answer['document_id'], content_data))
            if len(doc_list) > 0:
                doc = doc_list[0]
                meta_dict = doc.meta
                if len(meta_doc_list) > 0:
                    meta_doc = meta_doc_list[0]
                    meta_doc_dict = meta_doc.meta
                    meta_doc_dict.update(meta_dict)
                    meta_dict = meta_doc_dict

                answer.meta = meta_dict

            qas_docs.append(answer)

        return qas_docs


