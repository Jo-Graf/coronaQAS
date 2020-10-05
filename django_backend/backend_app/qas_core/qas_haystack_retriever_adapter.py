from typing import List
from haystack.retriever.base import BaseRetriever
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_document import QASDocument
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_retriever_variant import QASRetrieverVariant


class QASHaystackRetrieverAdapter(QASRetrieverVariant):

    def __init__(self, retriever:  BaseRetriever = None):
        self.__retriever = retriever

    def retrieve(self, query: str, database: QASDatabase) -> List[QASDocument]:

        database_variant = database.get_variant()

        if not isinstance(database_variant, QASHaystackDatabaseAdapter):
            raise AttributeError('QASHaystackRetrieverAdapter needs to be coupled with a QASHaystackDatabaseAdapter')

        doc_store = database_variant.get_document_store()

        self.__retriever.document_store = doc_store

        docs = self.__retriever.retrieve(query)

        qas_docs = []

        for doc in docs:
            qas_doc = QASDocument.doc_to_qas_doc(doc)
            qas_docs.append(qas_doc)

        return qas_docs
