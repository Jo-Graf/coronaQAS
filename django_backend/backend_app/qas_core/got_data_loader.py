# based on: https://haystack.deepset.ai/docs/latest/tutorial1md

from farm.file_utils import fetch_archive_from_http
from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor.utils import convert_files_to_dicts

from backend_app.qas_core.data_loader import DataLoader
# from haystack.indexing.cleaning import clean_wiki_text
# from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http
import sys


class GOTDataLoader(DataLoader):

    data_is_loaded = False

    def __init__(self):
        pass

    def data_is_loaded(self):
        return GOTDataLoader.data_is_loaded

    def load_data(self):
        # Let's first get some documents that we want to query
        # Here: 517 Wikipedia articles for Game of Thrones
        doc_dir = "../data/article_txt_got"
        s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"
        fetch_archive_from_http(url=s3_url, output_dir=doc_dir)

        dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)

        GOTDataLoader.data_is_loaded = True

        return dicts
