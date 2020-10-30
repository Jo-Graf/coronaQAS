from typing import List, Optional

from haystack import Document
from haystack.retriever.base import BaseRetriever
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_doc_type_enum import QASDocType
from backend_app.qas_core.qas_document import QASDocument
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_retriever_variant import QASRetrieverVariant


class QASHaystackRetrieverAdapter(QASRetrieverVariant):

    # TODO: add to uml
    top_k_value = 50

    def __init__(self, retriever:  BaseRetriever = None):
        self.__retriever = retriever

    # TODO: add param to uml
    def retrieve(self, query: str, database: QASDatabase, doc_type: Optional[QASDocType] = None) -> List[QASDocument]:

        database_variant = database.get_variant()

        if not isinstance(database_variant, QASHaystackDatabaseAdapter):
            raise AttributeError('QASHaystackRetrieverAdapter needs to be coupled with a QASHaystackDatabaseAdapter')

        doc_store = database_variant.get_document_store()

        self.__retriever.document_store = doc_store

        docs = self.__retriever.retrieve(query, top_k=QASHaystackRetrieverAdapter.top_k_value)

        qas_docs = []

        for doc in docs:
            if self._check_doc_type(doc, doc_type):
                qas_doc = QASDocument.doc_to_qas_doc(doc)
                qas_docs.append(qas_doc)

        return qas_docs

    def _check_doc_type(self, doc: Document, doc_type: Optional[QASDocType]) -> bool:

        meta = doc.meta

        if (meta is None) or ('is_doc_meta' not in meta.keys()) or ('is_doc_abstract' not in meta.keys()):
            return False

        is_meta = meta['is_doc_meta']
        is_abstract = meta['is_doc_abstract']

        if doc_type is None:
            return True
        elif doc_type == doc_type.META:
            return (is_meta is True) and (is_abstract is False)
        elif doc_type == doc_type.ABSTRACT:
            return (is_meta is False) and (is_abstract is True)
        elif doc_type == doc_type.SECTION:
            return (is_meta is False) and (is_abstract is False)
        elif doc_type == doc_type.TEXT:
            return is_meta is False
        else:
            raise AttributeError('Document-Type is not allowed')
