from __future__ import unicode_literals
from django.conf import settings
from audiofield.fields import AudioField
import os.path
from django.db import models


class Participant(models.Model):
    """
    This models saves all the survey answers for the
    elegibility of the participant in the song classification.
    """
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    age = models.IntegerField(default=15)
    gender = models.CharField(max_length=50, choices=[("Masculino", "Masculino",), ("Femenino", "Femenino")])


class SongClassification(models.Model):
    participant = models.ForeignKey(Participant)
    mood_label = models.CharField(max_length=300)


# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=300)
    genre = models.CharField(max_length=300)
    classifications = models.ManyToManyField(SongClassification)
    audio_file = models.FileField(upload_to='songs')

    # Add this method to your model
    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<ul class="playlist"><li style="width:250px;">\
            <a href="%s">%s</a></li></ul>' % (file_url, os.path.basename(self.audio_file.name))
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')

    def __unicode__(self):
        return self.name