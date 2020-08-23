import json

def get_question_selection():
    path_string = '/Users/Gino/Belegarbeit/django_backend/backend_app/resource/json/questions.json'
    file = open(path_string, 'r')
    return json.load(file)