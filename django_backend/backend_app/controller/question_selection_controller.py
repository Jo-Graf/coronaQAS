import json
from os import listdir
from os.path import isfile, join
import os

def get_question_selection():
    path_string = os.path.abspath('./backend_app/resource/json/questions.json')
    file = open(path_string, 'r')
    return json.load(file)