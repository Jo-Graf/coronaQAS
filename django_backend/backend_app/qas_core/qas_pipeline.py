# Connect to Elasticsearch
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.finder import Finder
from backend_app.qas_core.got_data_loader import GOTDataLoader
from haystack.retriever.sparse import ElasticsearchRetriever
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
# from haystack.utils import print_answers
from backend_app.qas_core.qas_data_loader import QASDataLoader
from backend_app.qas_core.qas_data_loader_variant import QASDataLoaderVariant
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_database_variant import QASDatabaseVariant
from backend_app.qas_core.qas_doc_type_enum import QASDocType
from backend_app.qas_core.qas_reader import QASReader
from backend_app.qas_core.qas_reader_variant import QASReaderVariant
from backend_app.qas_core.qas_retriever import QASRetriever
from backend_app.qas_core.qas_retriever_variant import QASRetrieverVariant


class QASPipelineObserver:

    def initialized(self):
        raise NotImplementedError('The initialized method of this observer class needs to be implemented')

    def answer_received(self, answer_json) -> object:
        raise NotImplementedError('The answer_received method of this observer class needs to be implemented')


class QASPipelineConfiguration:

    def __init__(self,
                 loader_variant: QASDataLoaderVariant,
                 database_variant: QASDatabaseVariant,
                 retriever_variant: QASRetrieverVariant,
                 reader_variant: QASReaderVariant):
        self.reader_variant = reader_variant
        self.retriever_variant = retriever_variant
        self.database_variant = database_variant
        self.loader_variant = loader_variant


class QASPipeline:
    observers = []
    database = None
    loader = None
    retriever = None
    reader = None
    # finder = None
    is_initialized = False
    configuration = None

    @staticmethod
    def set_configuration(config: QASPipelineConfiguration):
        QASPipeline.configuration = config

    @staticmethod
    def initialize():
        if not QASPipeline.configuration:
            raise AttributeError('QASPipeline.configuration must be set via set_configuration method')

        # loader
        QASPipeline.loader = QASDataLoader(variant=QASPipeline.configuration.loader_variant)
        # database
        QASPipeline.database = QASDatabase(variant=QASPipeline.configuration.database_variant, loader=QASPipeline.loader)
        # retriever
        QASPipeline.retriever = QASRetriever(variant=QASPipeline.configuration.retriever_variant)
        # reader
        QASPipeline.reader = QASReader(variant=QASPipeline.configuration.reader_variant)

        QASPipeline.is_initialized = True

        for observer in QASPipeline.observers:
            observer.initialized()

    @staticmethod
    def load_data():
        if not QASPipeline.is_initialized:
            QASPipeline.initialize()


    @staticmethod
    def add_observer(observer):
        QASPipeline.observers.append(observer)

    @staticmethod
    def remove_observer(observer):
        QASPipeline.observers.remove(observer)

    @staticmethod
    def ask_question(question):
        if not QASPipeline.is_initialized:
            QASPipeline.initialize()

        retrieved_docs = QASPipeline.retriever.retrieve(question,
                                                        QASPipeline.database,
                                                        QASDocType.TEXT,
                                                        load_doc_meta=True)

        answers = QASPipeline.reader.read(question, retrieved_docs)

        # filter unique answers
        unique_answers = {}
        for answer in answers:
            unique_answers[answer.answer_id] = answer

        # notify observers
        for observer in QASPipeline.observers:
            observer.answer_received(unique_answers.values())

        return unique_answers.values()
