import json
from pathlib import Path
from typing import List

from backend_app.qas_core.qas_data_loader_variant import QASDataLoaderVariant
from backend_app.qas_core.qas_document import QASDocument

# TODO: add class to uml


class QASCORD19DataLoaderVariant(QASDataLoaderVariant):

    def load_data(self) -> (bool, List[QASDocument]):

        clean_func = None

        file_paths = [p for p in Path(self._source_path).glob("**/*")][:10]

        documents = []

        for path in file_paths:

            if path.name.startswith('.'):
                continue

            json_data = None

            if path.suffix.lower() == ".json":
                with open(str(path)) as f:
                    json_data = json.load(f)
            else:
                raise Exception(f"Indexing of {path.suffix} files is not currently supported.")

            doc_id = json_data['paper_id']

            # add meta
            meta_doc_dict = json_data['metadata']
            meta_doc_dict['bib_entries'] = json_data['bib_entries']
            meta_doc_dict['ref_entries'] = json_data['ref_entries']
            meta_doc_dict['is_doc_meta'] = True
            meta_doc_dict['is_doc_abstract'] = False

            meta_doc = QASDocument(
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
                    'title': abstract['section'],
                    'cite_spans': abstract['cite_spans'],
                    'ref_spans': abstract['ref_spans'],
                    'is_doc_meta': False,
                    'is_doc_abstract': True
                }

                abstract_doc = QASDocument(
                    id=doc_id,
                    text=(clean_func(abstract['text']) if clean_func else abstract['text']),
                    meta=abstract_doc_dict
                )
                documents.append(abstract_doc)
                abstract_count += 1

            # add sections
            section_count = 0
            for section in json_data['body_text']:
                section_doc_dict = {
                    'section_count': section_count,
                    'title': section['section'],
                    'cite_spans': section['cite_spans'],
                    'ref_spans': section['ref_spans'],
                    'is_doc_meta': False,
                    'is_doc_abstract': False

                }

                section_doc = QASDocument(
                    id=doc_id,
                    text=(clean_func(section['text']) if clean_func else section['text']),
                    meta=section_doc_dict
                )
                documents.append(section_doc)
                section_count += 1

        return (len(documents) > 0), documents
