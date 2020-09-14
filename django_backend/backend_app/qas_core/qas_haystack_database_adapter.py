from typing import List

from haystack.database.base import BaseDocumentStore

from backend_app.qas_core.qas_database_variant import QASDatabaseVariant
from backend_app.qas_core.qas_document import QASDocument


class QASHaystackDatabaseAdapter(QASDatabaseVariant):

    def __init__(self, document_store:  BaseDocumentStore = None):
        self.__document_store = document_store

    def add_data(self, data: List[QASDocument]):
        self.__document_store.write_documents(data)

    def get_data(self) -> List[QASDocument]:
        return self.__document_store.get_all_documents()
