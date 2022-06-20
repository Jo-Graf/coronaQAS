# based on: https://haystack.deepset.ai/docs/latest/tutorial1md

from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.reader.farm import FARMReader
from haystack.retriever.sparse import ElasticsearchRetriever

from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_got_data_loader import QASGOTDataLoaderVariant
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_haystack_reader_adapter import QASHaystackReaderAdapter
from backend_app.qas_core.qas_haystack_retriever_adapter import QASHaystackRetrieverAdapter

from backend_app.qas_core.qas_reader import QASReader
from backend_app.qas_core.qas_retriever import QASRetriever


print('### qas reader test start ###')
# variable
dir_path = '' # path to got texts
url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"
question = 'Who is the mother of Sansa Stark?'
model_name = 'deepset/roberta-base-squad2'

# loader
loader = QASGOTDataLoaderVariant(url, dir_path)

# database
document_store = ElasticsearchDocumentStore(host='localhost', username='', password='', index='document')
database_variant = QASHaystackDatabaseAdapter(document_store=document_store)
database = QASDatabase(variant=database_variant, loader=loader)
database.load_data()

# retriever
haystack_retriever = ElasticsearchRetriever(None)
retriever_variant = QASHaystackRetrieverAdapter(retriever=haystack_retriever)
retriever = QASRetriever(variant=retriever_variant)
retrieved_docs = retriever.retrieve(question, database)

# reader
haystack_reader = FARMReader(model_name_or_path=model_name, use_gpu=False)
reader_variant = QASHaystackReaderAdapter(reader=haystack_reader)
reader = QASReader(variant=reader_variant)
answers = reader.read(question, retrieved_docs)

print(answers)

print('### qas retriever test end ###')
