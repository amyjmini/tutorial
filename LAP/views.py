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
from rest_framework.decorators import api_view

from .forms import FileForm
from LAP.models import FileModel
from LAP.serializers import FileSerializer

from music21 import converter
from music21 import midi
from music21 import note, stream, duration

from models.MuseGAN import MuseGAN
from models.loaders import load_music


def home(request):
    context = {}
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_Valid():
            form.save()
            return redirect(endPage)
    else:
        form = FileForm()
    return render(request, 'home.html', {'form': form})


@api_view(['POST'])
def download(request):
    model_name = 'our_model.h5'
    loaded_model = keras.models.load_model(os.path.join(settings.MODEL_ROOT, model_name))

    SECTION = 'compose'
    RUN_ID = '0017'
    DATA_NAME = 'chorales'
    FILENAME = 'Jsb16thSeparated.npz'
    RUN_FOLDER = 'run/{}/'.format(SECTION)
    RUN_FOLDER += '_'.join([RUN_ID, DATA_NAME])

    BATCH_SIZE = 64
    n_bars = 2
    n_steps_per_bar = 16
    n_pitches = 84
    n_tracks = 4
    data_binary, data_ints, raw_data = load_music(DATA_NAME, FILENAME, n_bars, n_steps_per_bar)

    gan = MuseGAN(input_dim=data_binary.shape[1:],
                  critic_learning_rate=0.001,
                  generator_learning_rate=0.001,
                  optimiser='adam',
                  grad_weight=10,
                  z_dim=32,
                  batch_size=BATCH_SIZE,
                  n_tracks=n_tracks,
                  n_bars=n_bars,
                  n_steps_per_bar=n_steps_per_bar,
                  n_pitches=n_pitches
                  )
    gan.load_weights(RUN_FOLDER, None)

    chords_noise = np.random.normal(0, 1, (1, gan.z_dim))
    style_noise = np.random.normal(0, 1, (1, gan.z_dim))
    melody_noise = np.random.normal(0, 1, (1, gan.n_tracks, gan.z_dim))
    groove_noise = np.random.normal(0, 1, (1, gan.n_tracks, gan.z_dim))
    gen_scores = gan.generator.predict([chords_noise, style_noise, melody_noise, groove_noise])

    np.argmax(gen_scores[0, 0, 0:4, :, 3], axis=1)
    filename = 'example'
    gan.notes_to_midi(RUN_FOLDER, gen_scores, filename)
    gen_score = converter.parse(os.path.join(RUN_FOLDER, 'samples/{}.midi'.format(filename)))
    gen_score.show()
    return Response('gen_score')


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
    template_name = 'loading.html'
    renderer_classes = [TemplateHTMLRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_name = 'our_model.h5'
        self.loaded_model = keras.models.load_model(os.path.join(settings.MODEL_ROOT, model_name))
        self.predictions = []

    def file_elaboration(self, filepath, request):
        # run params
        SECTION = 'compose'
        RUN_ID = '0017'
        DATA_NAME = 'chorales'
        FILENAME = 'Jsb16thSeparated.npz'
        RUN_FOLDER = 'run/{}/'.format(SECTION)
        RUN_FOLDER += '_'.join([RUN_ID, DATA_NAME])

        BATCH_SIZE = 64
        n_bars = 2
        n_steps_per_bar = 16
        n_pitches = 84
        n_tracks = 4
        data_binary, data_ints, raw_data = load_music(DATA_NAME, FILENAME, n_bars, n_steps_per_bar)

        gan = MuseGAN(input_dim=data_binary.shape[1:]
                      , critic_learning_rate=0.001
                      , generator_learning_rate=0.001
                      , optimiser='adam'
                      , grad_weight=10
                      , z_dim=32
                      , batch_size=BATCH_SIZE
                      , n_tracks=n_tracks
                      , n_bars=n_bars
                      , n_steps_per_bar=n_steps_per_bar
                      , n_pitches=n_pitches
                      )
        gan.load_weights(RUN_FOLDER, None)

        chords_noise = np.random.normal(0, 1, (1, gan.z_dim))
        style_noise = np.random.normal(0, 1, (1, gan.z_dim))
        melody_noise = np.random.normal(0, 1, (1, gan.n_tracks, gan.z_dim))
        groove_noise = np.random.normal(0, 1, (1, gan.n_tracks, gan.z_dim))
        gen_scores = gan.generator.predict([chords_noise, style_noise, melody_noise, groove_noise])

        np.argmax(gen_scores[0, 0, 0:4, :, 3], axis=1)
        filename = 'example'
        gan.notes_to_midi(RUN_FOLDER, gen_scores, filename)
        gen_score = converter.parse(os.path.join(RUN_FOLDER, 'samples/{}.midi'.format(filename)))
        gen_score.show()
        try:
            return Response({'score': gen_score.pop()}, status=status.HTTP_200_OK)
        except ValueError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
