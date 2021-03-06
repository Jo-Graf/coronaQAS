# based on: https://haystack.deepset.ai/docs/latest/tutorial1md

from typing import Optional, List
from uuid import uuid4
from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor.utils import fetch_archive_from_http, convert_files_to_dicts

from backend_app.qas_core.qas_data_loader_variant import QASDataLoaderVariant
from backend_app.qas_core.qas_document import QASDocument


class QASGOTDataLoaderVariant(QASDataLoaderVariant):
    """
    def __init__(self, source_path: Optional[str] = None, output_path: Optional[str] = None):
        self.__source_path = source_path
        self.__output_path = output_path
    """

    def load_data(self) -> (bool, List[QASDocument]):

        if (self._source_path is None) or (self._output_path is None):
            raise AttributeError('_source_path AND _output_path cannot be None')

        fetch_archive_from_http(url=self._source_path, output_dir=self._output_path)

        dicts = convert_files_to_dicts(dir_path=self._output_path, clean_func=clean_wiki_text, split_paragraphs=True)

        documents = []

        for dic in dicts:
            new_doc = QASDocument(text=dic['text'], meta=dic['meta'])
            documents.append(new_doc)

        return True, documents
