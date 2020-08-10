from django.shortcuts import render
from django.http import HttpResponse
from backend_app.forms import NameForm
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.express as px

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
        form = NameForm()

    df = px.data.iris()
    figure = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                     size='petal_length', hover_data=['petal_width'])
    graph = figure.to_html(full_html=False, default_height=500, default_width=700)

    context = {
        'form': form,
        'graph': graph
    }

    return render(request, 'test.html', context)
