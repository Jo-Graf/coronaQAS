from backend_app.qas_core.qas_got_data_loader import QASGOTDataLoaderVariant

print('### qas retriever test start ###')

dir = "/Users/Gino/Belegarbeit/django_backend/backend_app/data/article_txt_got"
url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"

loader = QASGOTDataLoaderVariant(url, dir)
loader.load_data()

print('### qas retriever test end ###')
