# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from music.forms import *
from django.db.models import Count
from music.models import *
from django.shortcuts import render
from django.conf import settings
import random
# Create your views here.


def pick_random_song_lowest_classifications():
    songs = Song.objects.annotate(num_classifications=Count('classifications')).order_by('num_classifications')
    lowest_song_num = songs[0].num_classifications
    selected_songs = []
    for s in songs:
        if s.num_classifications <= lowest_song_num:
            selected_songs.append(s)

    song = random.choice(selected_songs)
    return song


def get_songs_for_classification(request):
    """
    Selects 10 random songs that have the least amount of classifications.
    :param request:
    :return:
    """
    pass


def index(request):
    form = ParticipantForm()
    return render(request, 'music/home.html',{'participant_form': form})


def consentimiento_informado(request):
    return render(request, 'music/privacy-policy.html', {})


def song_classification(request):
    print request.POST
    if request.method == 'POST':
        # Create and save new classification
        participant = Participant.objects.get(pk=int(request.POST['participant_pk']))
        if request.POST['time']:
            time = float(request.POST['time'])
        classification = SongClassification(participant=participant, mood_label=request.POST['mood'])
        classification.time_taken = time
        classification.save()
        classified_song = Song.objects.get(pk=int(request.POST['song_pk']))
        classified_song.classifications.add(classification)
        classified_song.save()

        if int(request.POST['song_number']) == 10:
            # Redirect to thank you page
            return render(request, 'music/thank_you.html', {})
        else:
            # Get first song with lowest number of classifications
            song = pick_random_song_lowest_classifications()
            #song = Song.objects.get(pk=759)
            song_number = int(request.POST['song_number']) + 1
            return render(request, 'music/song_classification.html', {'song_number': song_number,
                                                                      'song': song,
                                                                      'num_songs': range(1, 11),
                                                                      'participant': participant})

    song = None
    return render(request, 'music/song_classification.html', {'song': song})


def start_classification(request):
    if request.method == "POST":
        participant_form = ParticipantForm(request.POST)
        if participant_form.is_valid():
            if participant_form.cleaned_data['email'] != "" and \
                    Participant.objects.filter(email=participant_form.cleaned_data['email']).exists():

                participant = Participant.objects.get(email=participant_form.cleaned_data['email'])
            else:
                participant = participant_form.save()

            # Get first song with lowest number of classifications
            # song = Song.objects.annotate(num_classifications=Count('classifications')).order_by('num_classifications')[0]
            song = pick_random_song_lowest_classifications()
            #song = Song.objects.get(pk=759)
            #return render(request, 'music/thank_you.html', {})
            return render(request, 'music/song_classification.html', {'song_number': 1,
                                                                      'song': song,
                                                                      'num_songs': range(1, 11),
                                                                      'participant': participant})
        else:
            form = ParticipantForm()
            return render(request, 'music/home.html', {'participant_form': participant_form})