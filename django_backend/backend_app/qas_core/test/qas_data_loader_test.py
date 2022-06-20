# based on: https://haystack.deepset.ai/docs/latest/tutorial1md

from backend_app.qas_core.got_data_loader import GOTDataLoader
from backend_app.qas_core.qas_got_data_loader import QASGOTDataLoaderVariant

print('### qas data loader test start ###')

dir_path = '' # path to got texts
url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"

loader = QASGOTDataLoaderVariant(url, dir_path)
loaded, data = loader.load_data()

print(len(data))

print(data[0].meta)

print('### qas data loader test end ###')

