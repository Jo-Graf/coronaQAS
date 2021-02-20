from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.reader.farm import FARMReader
from haystack.retriever.sparse import ElasticsearchRetriever

from backend_app.qas_core.qas_cord19_data_loader_variant import QASCORD19DataLoaderVariant
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_haystack_reader_adapter import QASHaystackReaderAdapter
from backend_app.qas_core.qas_haystack_retriever_adapter import QASHaystackRetrieverAdapter
from backend_app.qas_core.qas_pipeline import QASPipelineConfiguration, QASPipeline
from config import DATA_PATH, MODEL_NAME, DB_INDEX_NAME, DB_HOST, ANSWER_CONTEXT_LENGTH, DB_MAX_FIELDS

import json
import os


def main():
    initial_data_load_json_path = './backend_app/resource/json/initial_data_load.json'
    with open(initial_data_load_json_path) as f:
        initial_data_load_json = json.load(f)

    did_load = initial_data_load_json['loaded']

    if did_load:
        print('data already loaded')
        return

    load_data()

    initial_data_load_json['loaded'] = True

    with open(initial_data_load_json_path, 'w') as f:
        json.dump(initial_data_load_json, f)


def load_data():
    print('start data loading')
    dir_path = os.path.abspath(DATA_PATH)
    model_name = MODEL_NAME

    # loader
    loader_variant = QASCORD19DataLoaderVariant(dir_path)

    # database
    document_store = ElasticsearchDocumentStore(host=DB_HOST, username='', password='', index=DB_INDEX_NAME)
    database_variant = QASHaystackDatabaseAdapter(document_store=document_store)

    os.system('curl -X PUT db:9200/' +
              DB_INDEX_NAME +
              '/_settings -H \'Content-Type: application/json\' -d\'{\"index.mapping.total_fields.limit\": ' +
              str(DB_MAX_FIELDS) +
              '}\'')

    # retriever
    haystack_retriever = ElasticsearchRetriever(None)
    retriever_variant = QASHaystackRetrieverAdapter(retriever=haystack_retriever)

    # reader
    haystack_reader = FARMReader(model_name_or_path=model_name, use_gpu=False, context_window_size=ANSWER_CONTEXT_LENGTH)
    reader_variant = QASHaystackReaderAdapter(reader=haystack_reader)

    config = QASPipelineConfiguration(loader_variant,
                                      database_variant,
                                      retriever_variant,
                                      reader_variant)

    QASPipeline.set_configuration(config)

    QASPipeline.load_data()


if __name__ == '__main__':
    main()
