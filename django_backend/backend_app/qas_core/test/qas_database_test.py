# based on: https://haystack.deepset.ai/docs/latest/tutorial1md

from haystack.database.elasticsearch import ElasticsearchDocumentStore
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_got_data_loader import QASGOTDataLoaderVariant
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter

print('### qas database test start ###')

dir_path = '' # path to got texts
url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"

loader = QASGOTDataLoaderVariant(url, dir_path)
loaded, data = loader.load_data()

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
database_variant = QASHaystackDatabaseAdapter(document_store=document_store)
database = QASDatabase(variant=database_variant)
database.add_data(data)
data = database.get_data()

print(type(data))
print(len(data))
first_data = data[0]
print(type(first_data))
print(first_data.id)
print(first_data.text)
print(first_data.meta)
print(first_data)

print('### qas database test end ###')
