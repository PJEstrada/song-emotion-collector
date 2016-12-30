from django.shortcuts import render
from django.http import Http404
from music.forms import *
from django.db.models import Count
from music.models import *
from django.shortcuts import render
# Create your views here.


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


def song_classification(request):

    if request.method == 'POST':
        # Create and save new classification
        participant = Participant.objects.get(pk=int(request.POST['participant_pk']))
        classification = SongClassification(participant=participant, mood_label=request.POST['mood'])
        classification.save()
        classified_song = Song.objects.get(pk=int(request.POST['song_pk']))
        classified_song.classifications.add(classification)
        classified_song.save()

        if int(request.POST['song_number']) == 10:
            # Redirect to thank you page
            return render(request, 'music/thank_you.html', {})
        else:
            # Get first song with lowest number of classifications
            song = Song.objects.annotate(num_classifications=Count('classifications')).order_by('num_classifications')[0]
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
        participant = participant_form.save()

        # Get first song with lowest number of classifications
        song = Song.objects.annotate(num_classifications=Count('classifications')).order_by('num_classifications')[0]
        return render(request, 'music/song_classification.html', {'song_number': 1,
                                                                  'song': song,
                                                                  'num_songs': range(1,11),
                                                                  'participant': participant})
