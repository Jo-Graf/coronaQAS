# Connect to Elasticsearch
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from backend_app.qas_core.got_data_loader import GOTDataLoader
from haystack.retriever.sparse import ElasticsearchRetriever
from haystack import Finder
from haystack.indexing.cleaning import clean_wiki_text
from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers


class QASPipeline:
    observers = []
    document_store = None
    data_loader = None
    retriever = None
    reader = None
    finder = None
    is_initialized = False

    @staticmethod
    def initialize():
        QASPipeline.document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
        QASPipeline.data_loader = GOTDataLoader()

        if not QASPipeline.data_loader.data_is_loaded():
            dicts = QASPipeline.data_loader.load_data()
            QASPipeline.document_store.write_documents(dicts)

        QASPipeline.retriever = ElasticsearchRetriever(document_store=QASPipeline.document_store)
        QASPipeline.reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)
        QASPipeline.finder = Finder(QASPipeline.reader, QASPipeline.retriever)

        QASPipeline.is_initialized = True

        for observer in QASPipeline.observers:
            observer.initialized()

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

        prediction = QASPipeline.finder.get_answers(question=question, top_k_retriever=20, top_k_reader=10)

        for observer in QASPipeline.observers:
            observer.answer_received(prediction)

        return prediction


# async variant
class QASPipelineObserver:

    def initialized(self):
        raise NotImplementedError('The initialized method of this observer class needs to be implemented')

    def answer_received(self, answer_json) -> object:
        raise NotImplementedError('The answer_received method of this observer class needs to be implemented')
