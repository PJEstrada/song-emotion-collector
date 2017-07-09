# -*- coding: utf-8 -*-
"""
KNN - All data.
Este clasificador utilizará todos los frames de la canción sin nigun análisis estadísitico
dentro del modelo. Para determinar la emoción de una canción se utilizará la moda de todos los
frames clasificados dentro de la canción.
"""
from music.models import Song
from utils.services import load_song_features
import numpy as np
from sklearn import preprocessing, cross_validation, neighbors


def remove_std_from_features(features):
    result = []
    for i in range(0, len(features)/2):
        result.append(features[i])
    return np.array(result)

all_songs = Song.objects.all()
X = []
Y = []
for song in all_songs:
    song_features_per_fame = load_song_features(song)
    # song_features_per_fame = remove_std_from_features(song_features_per_fame)
    song_features_per_fame = song_features_per_fame.transpose()
    for i in range(0, len(song_features_per_fame)): # For each frame in the song.
         Y.append(song.genre)
    for i in range(0, len(song_features_per_fame)):
        # print len(frame_features)
        X.append(song_features_per_fame[i][0:50])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.2)

classifier = neighbors.KNeighborsClassifier()
classifier.fit(X_train, y_train)
accuracy = classifier.score(X_test, y_test)
print accuracy

