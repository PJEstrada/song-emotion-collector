# -*- coding: utf-8 -*-
from music.models import Song
import operator

results = []
results_classified = []
for song in Song.objects.all():

    classifications = song.classifications.all()
    if len(classifications) < 3:
        results.append(song.pk)
    else:
        # Get major classification
        emotion_counts = {'alegria': 0, 'tristeza': 0, 'enojo': 0, 'miedo': 0, 'neutral': 0}
        for c in classifications:
            try:
                emotion_counts[c.mood_label] += 1
            except:
                print "Cannot find emotion: "+c.mood_label


        max_element_key = max(emotion_counts.iteritems(), key=operator.itemgetter(1))[0]
        if max_element_key == 'neutral':
            results.append(song.pk)
        results_classified.append({'song': song, 'emotion': max_element_key})

print "PENDING SONGS"
print len(results)
print "CLASSIFIED SONGS"
for x in results_classified:
    print x
    x['song'].mood = x['emotion']
    x['song'].save()


