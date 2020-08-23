from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from backend_app.controller.question_selection_controller import get_question_selection
from backend_app.forms import NameForm
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.express as px
import json

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
        context = {
        }
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
        return HttpResponseRedirect('/index/')

