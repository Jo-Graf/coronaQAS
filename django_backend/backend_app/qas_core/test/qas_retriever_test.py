from haystack.database.elasticsearch import ElasticsearchDocumentStore

from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_got_data_loader import QASGOTDataLoaderVariant
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter

print('### qas retriever test start ###')

dir_path = "/Users/Gino/Belegarbeit/django_backend/backend_app/data/article_txt_got"
url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"

loader = QASGOTDataLoaderVariant(url, dir_path)

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
database_variant = QASHaystackDatabaseAdapter(document_store=document_store)
database = QASDatabase(variant=database_variant)



print('### qas retriever test end ###')
