from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.reader.farm import FARMReader
from haystack.retriever.sparse import ElasticsearchRetriever

from backend_app.controller.question_selection_controller import get_question_selection
from backend_app.forms import NameForm
import json
import hashlib

from backend_app.qas_core.pipeline import QASPipeline
from backend_app.qas_core.qas_cord19_data_loader_variant import QASCORD19DataLoaderVariant
from backend_app.qas_core.qas_data_loader import QASDataLoader
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_doc_type_enum import QASDocType
from backend_app.qas_core.qas_got_data_loader import QASGOTDataLoaderVariant
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_haystack_reader_adapter import QASHaystackReaderAdapter
from backend_app.qas_core.qas_haystack_retriever_adapter import QASHaystackRetrieverAdapter
from backend_app.qas_core.qas_lda import QASLDA
from backend_app.qas_core.qas_reader import QASReader
from backend_app.qas_core.qas_retriever import QASRetriever


def index(request):
	# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/admin/')

    # if a GET (or any other method) we'll create a blank form
    else:
        context = {}
        return render(request, 'test.html', context)


def question_selection(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/index/')
    else:
        json_question_selection = get_question_selection()
        return JsonResponse(json_question_selection, safe=False)


def qas(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/index/')
    else:
        '''
        question = json.loads(request.body)['question']

        # dir_path = "/Users/Gino/Belegarbeit/django_backend/backend_app/data/article_txt_got"
        # url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"
        dir_path = '/Volumes/glpstorage/Users/Gino/Belegarbeit/archive/document_parses/pdf_json_test/'
        model_name = 'NeuML/bert-small-cord19-squad2'

        # loader
        # loader = QASGOTDataLoaderVariant(url, dir_path)
        loader = QASCORD19DataLoaderVariant(dir_path)

        # database
        document_store = ElasticsearchDocumentStore(host='localhost', username='', password='', index='med_docs')
        database_variant = QASHaystackDatabaseAdapter(document_store=document_store)
        database = QASDatabase(variant=database_variant, loader=loader)
        # database.load_data()

        # retriever
        haystack_retriever = ElasticsearchRetriever(None)
        retriever_variant = QASHaystackRetrieverAdapter(retriever=haystack_retriever)
        retriever = QASRetriever(variant=retriever_variant)
        retrieved_docs = retriever.retrieve(question, database, QASDocType.TEXT)

        # reader
        haystack_reader = FARMReader(model_name_or_path=model_name, use_gpu=False)
        reader_variant = QASHaystackReaderAdapter(reader=haystack_reader)
        reader = QASReader(variant=reader_variant)
        answers = reader.read(question, retrieved_docs)

        # return unique answers
        unique_answers = {}
        for answer in answers:
            unique_answers[answer.answer_id] = answer.serialize()

        print(json.dumps(list(unique_answers.values())))
        return JsonResponse(list(unique_answers.values()), safe=False)
        '''
        dump_path = '/Users/Gino/Belegarbeit/django_backend/backend_app/resource/json/result_dump.json'
        json_dump = None
        with open(dump_path, 'r') as json_file:
            json_dump = json.load(json_file)

        return JsonResponse(json_dump, safe=False)

def lda(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/index/')
    else:

        doc_id = json.loads(request.body)['doc_id']
        doc_ids = json.loads(request.body)['doc_ids']
        print(doc_ids)

        '''
        # loader
        loader_variant = QASCORD19DataLoaderVariant(None)
        loader = QASDataLoader(variant=loader_variant)

        # database
        document_store = ElasticsearchDocumentStore(host='localhost', username='', password='', index='med_docs')
        database_variant = QASHaystackDatabaseAdapter(document_store=document_store)
        database = QASDatabase(variant=database_variant, loader=loader)

        # get base key
        base_key = loader.get_doc_base_key(key=doc_id)

        # query
        query = {
            "query": {
                "script": {
                    "script": "doc['_id'][0].indexOf('" + base_key + "') > -1"
                }
            }
        }

        # lda
        lda_instance = QASLDA(database=database, query=query)
        topics = lda_instance.load()
        '''
        topics = [
            ['word 1', 'word 2', 'word 3', 'word 4', 'word 5','word 1', 'word 2', 'word 3', 'word 4', 'word 5', 'word 1', 'word 2', 'word 3', 'word 4', 'word 5','word 1', 'word 2', 'word 3', 'word 4', 'word 5'],
            ['word 1', 'word 2', 'word 3', 'word 4', 'word 5'],
            ['word 1', 'word 2', 'word 3', 'word 4', 'word 5'],
            ['word 1', 'word 2', 'word 3', 'word 4', 'word 5'],
            ['word 1', 'word 2', 'word 3', 'word 4', 'word 5']
        ]
        return JsonResponse(topics, safe=False)
