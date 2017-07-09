# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from music import views

urlpatterns = [

    url(
        r'^$',
        views.index,
        name='index'
    ),
    # Consentimiento informado
    url(
        r'^privacy-policy',
        views.consentimiento_informado,
        name='consentimiento_informado'
    ),
    url(
        r'^classify',
        views.song_classification,
        name='song_classification'
    ),
    url(
        r'^explore',
        views.explore,
        name='explore'
    ),
    url(
        r'^start-classification',
        views.start_classification,
        name='start_classification'
    ),
]
