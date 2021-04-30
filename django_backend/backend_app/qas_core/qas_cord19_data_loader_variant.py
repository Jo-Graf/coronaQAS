import json
import os
from os import listdir
from pathlib import Path
from typing import List, Optional

from haystack import Document

from backend_app.qas_core.qas_data_loader_variant import QASDataLoaderVariant
from backend_app.qas_core.qas_doc_key_gen import QASDocKeyGen
from backend_app.qas_core.qas_document import QASDocument
from config import MAX_DOCS_LOAD


class QASCORD19DataLoaderVariant(QASDataLoaderVariant):

    doc_separator = "-$-$-"

    def load_data(self) -> (bool, List[QASDocument]):

        clean_func = None

        file_paths = [p for p in Path(self._source_path).glob("**/*")][:MAX_DOCS_LOAD]

        documents = []

        for path in file_paths:

            if path.name.startswith('.'):
                continue

            curr_docs = self.docs_from_path(path)

            documents.extend(curr_docs)

        return (len(documents) > 0), documents

    @staticmethod
    def docs_from_path(path: str) -> List[QASDocument]:
        clean_func = None
        documents = []
        doc_count = 1

        if path.name.startswith('.'):
            return documents

        json_data = None

        if path.suffix.lower() == ".json":
            with open(str(path)) as f:
                json_data = json.load(f)
        else:
            raise Exception(f"Indexing of {path.suffix} files is not currently supported.")

        doc_id = json_data['paper_id']
        title = json_data['metadata']['title']

        # add meta
        meta_doc_dict = json_data['metadata']
        # TODO: decide if authors are useful
        # meta_doc_dict['authors'] = None
        meta_doc_dict['bib_entries'] = QASCORD19DataLoaderVariant._cut_bib_ref(json_data['bib_entries'])
        # TODO: decide if ref entries are useful
        # meta_doc_dict['ref_entries'] = json_data['ref_entries']
        meta_doc_dict['is_doc_meta'] = True
        meta_doc_dict['is_doc_abstract'] = False

        meta_doc = Document(
            id=doc_id,
            text=None,
            meta=meta_doc_dict
        )
        documents.append(meta_doc)

        # add abstracts
        abstract_count = 0
        for abstract in json_data['abstract']:
            abstract_doc_dict = {
                'abstract_count': abstract_count,
                'title': title,
                'subtitle': abstract['section'],
                'cite_spans': QASCORD19DataLoaderVariant._cut_cite_span_texts(abstract['cite_spans']),
                # TODO: decide if ref spans are useful
                # 'ref_spans': abstract['ref_spans'],
                'is_doc_meta': False,
                'is_doc_abstract': True
            }

            abstract_doc = Document(
                id=QASDocKeyGen.generate_key(QASDocKeyGen.get_doc_base_key(key=doc_id), doc_count), #doc_id + QASCORD19DataLoaderVariant.doc_separator + str(doc_count),
                text=(clean_func(abstract['text']) if clean_func else abstract['text']),
                meta=abstract_doc_dict
            )
            documents.append(abstract_doc)
            abstract_count += 1
            doc_count += 1

        # add sections
        section_count = 0
        for section in json_data['body_text']:
            section_doc_dict = {
                'section_count': section_count,
                'title': title,
                'subtitle': section['section'],
                'cite_spans': QASCORD19DataLoaderVariant._cut_cite_span_texts(section['cite_spans']),
                # TODO: decide if ref spans are useful
                # 'ref_spans': section['ref_spans'],
                'is_doc_meta': False,
                'is_doc_abstract': False

            }

            section_doc = Document(
                id=QASDocKeyGen.generate_key(QASDocKeyGen.get_doc_base_key(key=doc_id), doc_count), # doc_id + QASCORD19DataLoaderVariant.doc_separator + str(doc_count),
                text=(clean_func(section['text']) if clean_func else section['text']),
                meta=section_doc_dict
            )

            documents.append(section_doc)
            section_count += 1
            doc_count += 1

        return documents

    @staticmethod
    def _cut_bib_ref(bib_entries: list):

        if not isinstance(bib_entries, dict):
            return bib_entries

        for key in bib_entries.keys():
            bib_entries[key].pop('authors', None)
            bib_entries[key].pop('venue', None)
            bib_entries[key].pop('volume', None)
            bib_entries[key].pop('issn', None)
            bib_entries[key].pop('other_ids', None)

        return bib_entries

    @staticmethod
    def _cut_cite_span_texts(cite_spans: list):
        if cite_spans is not list:
            return cite_spans

        for entry in cite_spans:
            cite_spans.pop('text', None)

        return cite_spans

    def get_doc_base_key(self, doc: Optional[QASDocument] = None, key: Optional[str] = None) -> str:

        return QASDocKeyGen.get_doc_base_key(doc=doc, key=key)