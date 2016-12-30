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
    url(
        r'^classify',
        views.song_classification,
        name='song_classification'
    ),
    url(
        r'^start-classification',
        views.start_classification,
        name='start_classification'
    ),
]
