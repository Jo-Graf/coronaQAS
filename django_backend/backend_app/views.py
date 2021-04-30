from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.reader.farm import FARMReader
from haystack.retriever.sparse import ElasticsearchRetriever
import django.contrib

from backend_app.controller.question_selection_controller import get_question_selection
from backend_app.forms import NameForm
import json

from backend_app.models import Doc
from backend_app.qas_core.qas_pipeline import QASPipeline, QASPipelineConfiguration
from backend_app.qas_core.qas_cord19_data_loader_variant import QASCORD19DataLoaderVariant
from backend_app.qas_core.qas_data_loader import QASDataLoader
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_doc_key_gen import QASDocKeyGen
from backend_app.qas_core.qas_haystack_database_adapter import QASHaystackDatabaseAdapter
from backend_app.qas_core.qas_haystack_reader_adapter import QASHaystackReaderAdapter
from backend_app.qas_core.qas_haystack_retriever_adapter import QASHaystackRetrieverAdapter
from backend_app.qas_core.qas_lda import QASLDA
import datetime


from config import DATA_PATH, MODEL_NAME, DB_INDEX_NAME, DB_HOST


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
        return render(request, 'ui.html', context)


def question_selection(request):

    now = datetime.datetime.now()

    if now.year != 2021 or now.month < 3 or now.month > 5:
        # quit()
        pass

    if request.method == 'POST':
        return HttpResponseRedirect('/index/')
    else:
        json_question_selection = get_question_selection()
        return JsonResponse(json_question_selection, safe=False)


def login(request):

    if request.method == 'GET':
        response = {
            'logged_in': request.user.is_authenticated,
            'username': request.user.username
        }

        return JsonResponse(response, safe=False)
    else:
        username = json.loads(request.body)['username']
        password = json.loads(request.body)['password']

        user = authenticate(request, username=username, password=password)

        response_dict = None

        if user is not None:
            django.contrib.auth.login(request, user)
            response_dict = {
                'success': True,
                'message': 'You\'ve been logged in'
            }
        else:
            response_dict = {
                'success': False,
                'message': 'Login didn\'t work please check username and password'
            }

        return JsonResponse(response_dict, safe=False)


def logout(request):
    django.contrib.auth.logout(request)
    response_dict = {
        'success': True,
        'message': 'You\'ve been logged out'
    }
    return JsonResponse(response_dict, safe=False)


def update_user_specific_doc_meta(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/index/')
    else:
        user_id = request.user.id
        note = json.loads(request.body)['doc_note']
        bookmarked = json.loads(request.body)['doc_bookmarked']
        doc_id = json.loads(request.body)['doc_id']
        base_doc_id = QASDocKeyGen.get_doc_base_key(key=doc_id)

        objects = Doc.objects.filter(user_id=user_id).filter(doc_id=base_doc_id)
        doc_object = objects[0] if len(objects) > 0 else Doc(doc_id=base_doc_id, user_id=user_id)

        if note is not None:
            doc_object.note = note

        if bookmarked is not None:
            doc_object.bookmarked = bookmarked

        doc_object.save()

        json_obj = json.loads(serializers.serialize('json', [doc_object]))[0]

        response = {
            'success': True,
            'message': 'Saving was successful',
            'user_specific_doc_meta': json_obj
        }

        print(response)

        return JsonResponse(response, safe=False)


def user_specific_doc_meta(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/index/')
    else:
        doc_id = None
        user_id = request.user.id
        if 'doc_id' in json.loads(request.body).keys():
            doc_id = json.loads(request.body)['doc_id']
            base_doc_id = QASDocKeyGen.get_doc_base_key(key=doc_id)

        objects = None

        if doc_id is None:
            objects = Doc.objects.filter(user_id=user_id)
        else:
            objects = Doc.objects.filter(user_id=user_id).filter(doc_id=base_doc_id)

        ids = [x.doc_id for x in objects]

        # loader
        loader_variant = QASCORD19DataLoaderVariant(None)
        loader = QASDataLoader(variant=loader_variant)

        # database
        document_store = ElasticsearchDocumentStore(host=DB_HOST, username='', password='', index=DB_INDEX_NAME)
        database_variant = QASHaystackDatabaseAdapter(document_store=document_store)
        database = QASDatabase(variant=database_variant, loader=loader)

        print(ids)
        docs = database.get_data(identifiers=ids)

        for doc in docs:
            print(doc.meta['title'])

        json_str = serializers.serialize('json', objects)
        json_obj = json.loads(json_str)

        for obj in json_obj:
            doc_list = list(filter(lambda x: x.id == obj['fields']['doc_id'],
                                   docs))
            if doc_list and len(doc_list) > 0:
                doc = doc_list[0]
                obj['fields']['meta'] = doc.meta
            else:
                print('no doc found for: ' + obj['fields']['doc_id'])

        json_str = json.dumps(json_obj)
        return HttpResponse(json_str, content_type="application/json")


def qas(request):

    if request.method == 'GET':
        return HttpResponseRedirect('/index/')
    else:
        question = json.loads(request.body)['question']
        dir_path = DATA_PATH
        model_name = MODEL_NAME

        # loader
        loader_variant = QASCORD19DataLoaderVariant(dir_path)

        # database
        document_store = ElasticsearchDocumentStore(host=DB_HOST, username='', password='', index=DB_INDEX_NAME)
        database_variant = QASHaystackDatabaseAdapter(document_store=document_store)

        # retriever
        haystack_retriever = ElasticsearchRetriever(None)
        retriever_variant = QASHaystackRetrieverAdapter(retriever=haystack_retriever)

        # reader
        haystack_reader = FARMReader(model_name_or_path=model_name, use_gpu=False, context_window_size=512)
        reader_variant = QASHaystackReaderAdapter(reader=haystack_reader)

        config = QASPipelineConfiguration(loader_variant,
                                          database_variant,
                                          retriever_variant,
                                          reader_variant)

        QASPipeline.set_configuration(config)
        answers = QASPipeline.ask_question(question)

        # return serialized answers
        serialized_answers = {}
        for answer in answers:
            serialized_answers[answer.answer_id] = answer.serialize()

        return JsonResponse(list(serialized_answers.values()), safe=False)

        '''
        dump_path = './django_backend/backend_app/resource/json/result_dump.json'
        json_dump = None
        with open(dump_path, 'r') as json_file:
            json_dump = json.load(json_file)
            
        return JsonResponse(json_dump, safe=False)

        '''

def lda(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/index/')
    else:

        doc_id = json.loads(request.body)['doc_id']
        doc_ids = json.loads(request.body)['doc_ids']

        # loader
        loader_variant = QASCORD19DataLoaderVariant(None)
        loader = QASDataLoader(variant=loader_variant)

        # database
        document_store = ElasticsearchDocumentStore(host=DB_HOST, username='', password='', index=DB_INDEX_NAME)
        database_variant = QASHaystackDatabaseAdapter(document_store=document_store)
        database = QASDatabase(variant=database_variant, loader=loader)

        # get base key
        base_key = loader.get_doc_base_key(key=doc_id)

        # query
        query = {"query": {"script": {"script": "doc['_id'][0].indexOf('" + base_key + "') > -1"}}}
        queries = [{"query": {"script": {"script": "doc['_id'][0].indexOf('" + x + "') > -1"}}}
                   for x in doc_ids]

        # lda
        lda_instance = QASLDA(database=database, doc_query=query, docs_queries=queries)
        topics = lda_instance.load()
        return JsonResponse(topics, safe=False)

        '''
        topics = {'id': '137a291fa34f85bf39cd25c1321a8cbbd9ccb30d',
         'topics': [{'words': ['disease',
                               'cardiometabolic',
                               'participants',
                               'hour',
                               'analysis',
                               'threat',
                               'plastic',
                               'surgery',
                               'health',
                               'qfpd',
                               'cognitive',
                               'performance',
                               'webinars',
                               'threats',
                               'study',
                               'restriction',
                               'prolonged',
                               'security',
                               'sitting',
                               'sleep'],
                     'probabilities': [0.0009456530982279886,
                                       0.000945653176014903,
                                       0.0009456641392426807,
                                       0.0009456676781580897,
                                       0.0009456742454180202,
                                       0.0010123803238211663,
                                       0.00104835142313254,
                                       0.0010493152405353539,
                                       0.0010700045661547735,
                                       0.0010790714921905629,
                                       0.0010790822665606174,
                                       0.0010790913321639451,
                                       0.0013157367355800685,
                                       0.0013459219672264946,
                                       0.0013459335437236376,
                                       0.0014126322397762974,
                                       0.0016127707364958581,
                                       0.0025467510640471104,
                                       0.00274680776216642,
                                       0.00274680776216642]},
                    {'words': ['private',
                               'women',
                               'literature',
                               'articles',
                               'sdgs',
                               'focus',
                               'individual',
                               'gender',
                               'public',
                               'agenda',
                               'health',
                               'ebp',
                               'sdg',
                               'evidence',
                               'positive',
                               'nurses',
                               'dual',
                               'practice',
                               'social',
                               'language'],
                     'probabilities': [0.0008679539505747064,
                                       0.0008755736694536914,
                                       0.0009298311010687653,
                                       0.0009404975335920849,
                                       0.0009420205749842601,
                                       0.0009420435938103641,
                                       0.0010001227932822823,
                                       0.0010075086168389398,
                                       0.0010678782482981828,
                                       0.0010707343484988115,
                                       0.001090760267401223,
                                       0.0011413803143080824,
                                       0.0012078335703582547,
                                       0.001299494768510673,
                                       0.0013407872186754573,
                                       0.0015337412274743579,
                                       0.0015337475209637615,
                                       0.0016269020566052666,
                                       0.001689333799140061,
                                       0.0027360364454714066]},
                    {'words': ['number',
                               'population',
                               'spread',
                               'countries',
                               'disease',
                               'cases',
                               'patients',
                               'world',
                               'time',
                               'measures',
                               'sars',
                               'public',
                               'impact',
                               'people',
                               'research',
                               'virus',
                               'data',
                               'social',
                               'pandemic',
                               'health'],
                     'probabilities': [0.0021213545806782696,
                                       0.002133223018973891,
                                       0.0021763633094105304,
                                       0.0021862791606148046,
                                       0.002285907523632305,
                                       0.002408754836842955,
                                       0.002445511162390494,
                                       0.002506645982982771,
                                       0.0025201778513839644,
                                       0.0026568115027071604,
                                       0.0030275722024720986,
                                       0.003240681926388003,
                                       0.003520371815836866,
                                       0.003551203602937314,
                                       0.0036184057593233536,
                                       0.0038983231146688135,
                                       0.00494520880629553,
                                       0.005038678835246527,
                                       0.00600049403508366,
                                       0.006455537570999651]},
                    {'words': ['united',
                               'possible',
                               'better',
                               'social',
                               'good',
                               'new',
                               'abstract',
                               'highlights',
                               'shock',
                               'like',
                               'making',
                               'positive',
                               'coronavirus',
                               'thoughts',
                               'time',
                               'know',
                               'way',
                               'place',
                               'training',
                               'self'],
                     'probabilities': [0.00017787799887719234,
                                       0.0001778780078699954,
                                       0.00017787807607363642,
                                       0.0001778780916040546,
                                       0.00017787813561687992,
                                       0.00017787818380856247,
                                       0.00017787822014002288,
                                       0.00017787826659042605,
                                       0.00017787840858461752,
                                       0.00017787848707491875,
                                       0.0001778785312912387,
                                       0.00017787855124577957,
                                       0.00017787866611143274,
                                       0.0001778787470680319,
                                       0.0001778788135857989,
                                       0.0001778790219334864,
                                       0.00017787905477658313,
                                       0.00017787911529966818,
                                       0.0001778798890782721,
                                       0.00017788079272559873]},
                    {'words': ['lot',
                               'text',
                               'speak',
                               'absorption',
                               'try',
                               'win',
                               'pelias',
                               'voices',
                               'destructive',
                               'dies',
                               'neoliberalism',
                               'strange',
                               'self',
                               'fear',
                               'shock',
                               'doctrine',
                               'feel',
                               'protest',
                               'write',
                               'intro'],
                     'probabilities': [0.00031926454585105905,
                                       0.00032573581285100207,
                                       0.0003258881064205577,
                                       0.00032588903465120204,
                                       0.00032588966807381886,
                                       0.00032588966807382504,
                                       0.0003258896680738273,
                                       0.0003258896680738278,
                                       0.00032588966807383014,
                                       0.0003258896680738307,
                                       0.00032588966807383106,
                                       0.0003258896680738317,
                                       0.0003615661349481993,
                                       0.0003654346582667783,
                                       0.00039473981226844013,
                                       0.00040419965830238797,
                                       0.00048337598361956067,
                                       0.0004833785710275644,
                                       0.0006430639313379515,
                                       0.0008036403384807627]},
                    {'words': ['current',
                               'incomes',
                               'minority',
                               'actions',
                               'personal',
                               'research',
                               'crisis',
                               'debt',
                               'work',
                               'heroism',
                               'implications',
                               'finance',
                               'workers',
                               'household',
                               'toleration',
                               'psychological',
                               'healthcare',
                               'corporate',
                               'tolerance',
                               'tolerated'],
                     'probabilities': [0.0008733543412537056,
                                       0.0009139474667351746,
                                       0.0009270820572857017,
                                       0.0009561954125976417,
                                       0.0009580676966403712,
                                       0.0009680090208717736,
                                       0.0009897914668938817,
                                       0.0009974311012889215,
                                       0.0010215782618565232,
                                       0.0010559546470040287,
                                       0.0010607851855255353,
                                       0.0010678007301295252,
                                       0.001069742806650995,
                                       0.0011287386631978855,
                                       0.0011381563767353042,
                                       0.001208531306274296,
                                       0.0012716159076902615,
                                       0.0013492489847783888,
                                       0.0013492519888387516,
                                       0.0018417773666010954]}],
         'topic_probabilities': [0.1, 0.2, 0.25, 0.3, 0.2, 0.05],#[5.32534587e-04, 5.31635161e-04, 9.97345108e-01, 5.29686384e-04, 5.30067330e-04, 5.30968900e-04],
         'nearest_neighbours': ['088c5ae25413cf52d45548a7a7d79e47077416e8',
                                '16f8d236817a757231007037bbf173f58d3cc42c',
                                '1f9a1e98b42ca167e9f0b8d7f4ea40df0770bc55']}
        return JsonResponse(topics, safe=False)
        '''