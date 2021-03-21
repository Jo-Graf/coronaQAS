from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.sparse import ElasticsearchRetriever

from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_got_data_loader import QASGOTDataLoaderVariant
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_haystack_retriever_adapter import QASHaystackRetrieverAdapter
from backend_app.qas_core.qas_retriever import QASRetriever

print('### qas retriever test start ###')

dir_path = '' # path to got texts
url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"
question = 'Who is the mother of Sansa Stark?'

loader = QASGOTDataLoaderVariant(url, dir_path)

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
database_variant = QASHaystackDatabaseAdapter(document_store=document_store)
database = QASDatabase(variant=database_variant, loader=loader)
database.load_data()

haystack_retriever = ElasticsearchRetriever(None)
retriever_variant = QASHaystackRetrieverAdapter(retriever=haystack_retriever)
retriever = QASRetriever(variant=retriever_variant)
result = retriever.retrieve(question, database)
print(result[0])

print('### qas retriever test end ###')
