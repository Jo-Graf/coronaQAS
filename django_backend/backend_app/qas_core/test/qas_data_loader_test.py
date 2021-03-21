from backend_app.qas_core.got_data_loader import GOTDataLoader
from backend_app.qas_core.qas_got_data_loader import QASGOTDataLoaderVariant

print('### qas data loader test start ###')

dir_path = '' # path to got texts
url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"

loader = QASGOTDataLoaderVariant(url, dir_path)
loaded, data = loader.load_data()

# TODO: add test for data count (2811)
print(len(data))

# TODO: add test for meta name field (145_Elio_M._García_Jr._and_Linda_Antonsson.txt)
print(data[0].meta)

print('### qas data loader test end ###')

