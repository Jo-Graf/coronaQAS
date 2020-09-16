from typing import List
from haystack.reader.base import BaseReader

from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_document import QASDocument
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_reader_variant import QASReaderVariant
from backend_app.qas_core.qas_retriever_variant import QASRetrieverVariant


class QASHaystackReaderAdapter(QASReaderVariant):

    def __init__(self, reader:  BaseReader = None):
        self.__reader = reader