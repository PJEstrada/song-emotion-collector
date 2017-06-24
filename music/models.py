# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django_countries.fields import CountryField
import os.path
from django.db import models

GENDERS = [("Masculino", "Masculino",), ("Femenino", "Femenino")]
YES_NO = [ ("No", "No"), ("Si", "Si",)]
SCOLARITY = [("Ninguno", "Ninguno",),
             ("Primaria", "Primaria"),
             ("Basicos", "Basicos"),
             ("Bachillerato", "Bachillerato"),
             ("Universitario", "Universitario"),
             ("Licenciatura", "Licenciatura"),
             (u"Maestrías/Doctorados", u"Maestrías/Doctorados")]


class Participant(models.Model):
    """
    This models saves all the survey answers for the
    elegibility of the participant in the song classification.
    """
    first_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=300)
    age = models.IntegerField(default=15)
    gender = models.CharField(max_length=50, choices=GENDERS, default=GENDERS[0])
    scolarity = models.CharField(max_length=50, choices=SCOLARITY, default=SCOLARITY[0])
    country = CountryField(blank_label='(Seleccione País)')
    knows_music_theory = models.CharField(choices=YES_NO, max_length=50, verbose_name="Posee concoimientos de teoría musical/armonía básica", default=YES_NO[1])
    has_physical_problem = models.CharField(choices=YES_NO, max_length=50, verbose_name="Posee impedimentos físicos", default=YES_NO[1])
    physical_problem = models.TextField(blank=True, null=True)
    hearing_problem = models.TextField(blank=True, null=True)
    has_hearing_problem = models.CharField(choices=YES_NO, max_length=50, verbose_name="Posee impedimentos Auditivos", default=YES_NO[1])
    psychological_problem = models.TextField(blank=True, null=True)
    has_psychological_problem = models.CharField(choices=YES_NO, max_length=50, verbose_name="Posee algún problema o desorden psicológico", default=YES_NO[1])
    is_uvg = models.BooleanField(blank=True, default=settings.UVG_STUDENT)


class SongClassification(models.Model):
    participant = models.ForeignKey(Participant)
    mood_label = models.CharField(max_length=300)
    date_taken = models.DateTimeField(auto_now=True)
    time_taken = models.FloatField(blank=True, null=True,default=0.0)


# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=300)
    genre = models.CharField(max_length=300)
    classifications = models.ManyToManyField(SongClassification)
    audio_file = models.FileField(upload_to='songs')
    s3_path = models.CharField(max_length=1000)
    cloud_front_path = models.CharField(max_length=1000)

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

    @property
    def key(self):
        return self.s3_path.split(settings.S3_URL)[1]