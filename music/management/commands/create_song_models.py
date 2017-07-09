# -*- coding: utf-8 -*-
from boto.s3.connection import S3Connection
from utils.services import log, log_title, log_subtitle
from music.models import Song
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates models for songs on S3"

    def handle(self, *args, **kwargs):
        print log_title("Load Songs Script")
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket('music-emotions')
        i = 0
        for key in bucket.list():
            genre = key.name.split("/", 1)[0]
            name = key.name.split("/", 1)[1]
            if genre == 'ambient':
                print log_subtitle("Loading Songs From Genre: 'Ambient' ")
            elif genre == 'pop':
                print log_subtitle("Loading Songs From Genre: 'Pop' ")
            elif genre == 'rock':
                print log_subtitle("Loading Songs From Genre: 'Rock' ")
            elif genre == 'blues-r&b':
                print log_subtitle("Loading Songs From Genre: 'Blues' ")
            elif genre == 'classical':
                print log_subtitle("Loading Songs From Genre: 'Classical' ")
            elif genre == 'country-folk':
                print log_subtitle("Loading Songs From Genre: 'Country Folk' ")
            elif genre == 'electronic':
                print log_subtitle("Loading Songs From Genre: 'Electronic' ")
            elif genre == 'hiphop':
                print log_subtitle("Loading Songs From Genre: 'Hip Hop' ")
            elif genre == 'jazz':
                print log_subtitle("Loading Songs From Genre: 'Jazz' ")
            else:
                continue
            print log("Creating song #"+str(i)+" : "+name)
            song = Song(name=name, genre=genre,
                        audio_file=unicode(key.name),
                        s3_path=unicode(settings.S3_URL+key.name),
                        cloud_front_path=unicode(settings.CLOUD_FRONT+key.name))
            song.save()
            i += 1
        print log("Finished :)")

