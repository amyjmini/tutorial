import os
from os import listdir
from os.path import join
from os.path import isfile
import requests

from django.shortcuts import render, redirect

from keras import backend as K
import tensorflow as tf
from django.conf import settings
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from rest_framework import views
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view

from .forms import FileForm
from LAP.models import FileModel
from LAP.serializers import FileSerializer

from music21 import midi

from models.MusicGenerator import MusicGenerator
import numpy as np

from django.core.files import File
from django.http import FileResponse

def home(request):
    return render(request, 'home.html')


@api_view(['GET'])
def download(request):
    return FileResponse(open('models/samples/example.midi', 'rb'), content_type='audio/midi')

def endPage(request):
    K.clear_session()
    filename = 'example'
    music_gen = MusicGenerator()
    score = music_gen.Generate()
    music_gen.notes_to_midi('models/', score, filename)

    return render(request, 'endPage.html')

def contactPage(request):
    return render(request, 'contactPage.html')