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
pending_pks = [4,
 9,
 20,
 22,
 24,
 33,
 37,
 38,
 39,
 41,
 42,
 48,
 50,
 53,
 55,
 60,
 63,
 76,
 77,
 78,
 89,
 93,
 95,
 101,
 102,
 110,
 121,
 128,
 129,
 131,
 134,
 137,
 160,
 164,
 168,
 170,
 172,
 174,
 178,
 181,
 186,
 202,
 203,
 204,
 205,
 209,
 213,
 225,
 230,
 237,
 239,
 245,
 248,
 249,
 252,
 258,
 267,
 272,
 273,
 275,
 281,
 282,
 290,
 292,
 297,
 299,
 301,
 303,
 307,
 308,
 309,
 314,
 317,
 320,
 325,
 327,
 329,
 334,
 335,
 337,
 339,
 341,
 358,
 359,
 360,
 363,
 365,
 366,
 369,
 371,
 381,
 387,
 388,
 390,
 391,
 396,
 405,
 418,
 419,
 423,
 425,
 429,
 430,
 431,
 436,
 437,
 447,
 456,
 460,
 463,
 466,
 478,
 482,
 486,
 487,
 492,
 493,
 494,
 496,
 498,
 500,
 501,
 507,
 510,
 511,
 520,
 525,
 530,
 536,
 539,
 542,
 543,
 544,
 547,
 551,
 552,
 556,
 558,
 560,
 562,
 567,
 568,
 569,
 575,
 578,
 587,
 592,
 593,
 598,
 601,
 602,
 606,
 607,
 608,
 610,
 613,
 616,
 625,
 630,
 635,
 644,
 647,
 649,
 650,
 653,
 655,
 661,
 672,
 676,
 677,
 678,
 681,
 682,
 683,
 686,
 688,
 691,
 700,
 701,
 702,
 709,
 711,
 714,
 719,
 720,
 721,
 723,
 728,
 733,
 735,
 736,
 747,
 749,
 754,
 761,
 763,
 769,
 777,
 780,
 782,
 785,
 787,
 788,
 791,
 799,
 805,
 812,
 814,
 816,
 817,
 832,
 834,
 835,
 837,
 841,
 845,
 847,
 851,
 856,
 857]


def pick_random_song_lowest_classifications():
    filtered_songs = Song.objects.filter(pk__in=pending_pks)
    # filtered_songs = Song.objects.all()
    songs = filtered_songs.annotate(num_classifications=Count('classifications')).order_by('num_classifications')
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


def explore(request):
    if 'genre' in request.GET:
        genre = request.GET['genre']
        if genre == 'blues-r':
            genre = 'blues-r&b'
        songs = Song.objects.filter(genre=genre)
    else:
        songs = Song.objects.filter(genre='ambient')
        genre = 'ambient'
    return render(request, 'music/explore.html', {'selected_genre':genre,
                                                  'genres':settings.GENRES,
                                                    'songs': songs})


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
            #song = Song.objects.get(pk=124)
            #return render(request, 'music/thank_you.html', {})
            return render(request, 'music/song_classification.html', {'song_number': 1,
                                                                      'song': song,
                                                                      'num_songs': range(1, 11),
                                                                      'participant': participant})
        else:
            form = ParticipantForm()
            return render(request, 'music/home.html', {'participant_form': participant_form})