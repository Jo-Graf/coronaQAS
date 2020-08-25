from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from backend_app.controller.question_selection_controller import get_question_selection
from backend_app.forms import NameForm
import json
import hashlib

from backend_app.qas_core.pipeline import QASPipeline


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
        question = json.loads(request.body)['question']
        # path_string = '/Users/Gino/Belegarbeit/django_backend/backend_app/resource/json/result_dump.json'
        # file = open(path_string, 'r')
        # response = json.load(file)
        response = QASPipeline.ask_question(question)

        unique_key_components = ['answer', 'offset_start_in_doc', 'offset_end_in_doc', 'context', 'probability', 'score']
        unique_answers = {}

        for answer in response['answers']:
            unique_key = ''.join([str(answer[x]) for x in unique_key_components]).encode('utf-8')
            unique_hashed_key = hashlib.md5(unique_key).hexdigest()
            unique_answers[unique_hashed_key] = answer

        response['answers'] = list(unique_answers.values())
        return JsonResponse(response, safe=False)

