import os
from os import listdir
from os.path import join
from os.path import isfile
import requests

from django.shortcuts import render, redirect

import keras
import tensorflow as tf
import numpy as np
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

from .forms import FileForm
from LAP.models import FileModel
from LAP.serializers import FileSerializer

from music21 import converter
from music21 import midi
from music21 import note, stream, duration

from models.MuseGAN import MuseGAN
from models.loaders import load_music




def home(request):
    context={}
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_Valid():
            form.save()
            return redirect(endPage)
    else:
        form = FileForm()
    return render(request, 'home.html', {'form': form})

def loadingPage(request):
    return render(request, 'loadingPage.html')

def endPage(request):
    return render(request, 'endPage.html')

def contactPage(request):
    return render(request, 'contactPage.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request, 'upload.html')

class Compose(views.APIView):
    template_name = 'home.html'
    renderer_classes = [TemplateHTMLRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_name = 'weights-c.h5'
        self.loaded_model = keras.models.load_model(os.path.join(settings.MODEL_ROOT, model_name))
        self.predictions = []


