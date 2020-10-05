from typing import List
from haystack.document_store.base import BaseDocumentStore
from backend_app.qas_core.qas_database_variant import QASDatabaseVariant
from backend_app.qas_core.qas_document import QASDocument


class QASHaystackDatabaseAdapter(QASDatabaseVariant):

    def __init__(self, document_store:  BaseDocumentStore = None):
        self.__document_store = document_store

    def get_document_store(self) -> BaseDocumentStore:
        return self.__document_store

    def add_data(self, data: List[QASDocument]):
        dict_list = []
        for doc in data:
            doc_as_dict = doc.to_dict()
            dict_list.append(doc_as_dict)
        self.__document_store.write_documents(dict_list)

    def get_data(self) -> List[QASDocument]:
        docs = self.__document_store.get_all_documents()
        qas_docs = []
        for doc in docs:
            qas_doc = QASDocument.doc_to_qas_doc(doc)
            qas_docs.append(qas_doc)
        return qas_docs
