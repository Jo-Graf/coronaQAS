from haystack.indexing.cleaning import clean_wiki_text
from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http

print('### qas retriever test start ###')

doc_dir = '../../data/article_txt_got'
s3_url = 'https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip'
fetch_archive_from_http(url=s3_url, output_dir=doc_dir)
dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
print(dicts)

print('### qas retriever test end ###')
