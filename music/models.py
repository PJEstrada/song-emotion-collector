from __future__ import unicode_literals

from django.db import models


class ParticipantProfile(models.Model):
    """
    This models saves all the survey answers for the
    elegibility of the participant in the song classification.
    """


class Participant(models.Model):
    first_name = models.CharField(max_length=300)


class SongClassification(models.Model):
    participant = models.ForeignKey(Participant)
    mood_label = models.CharField(max_length=300)


# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=300)
    genre = models.CharField(max_length=300)
    classifications = models.ManyToManyField(SongClassification)