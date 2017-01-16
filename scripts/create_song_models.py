from boto.s3.connection import S3Connection
from utils.services import log, log_title, log_subtitle
from music.models import Song

print log_title("Load Songs Script")
conn = S3Connection('AKIAIYHCCSRSMGEISPUQ','sFhSpLWG+7oI8xySrHgINxCO9BH5n/N2ImykurL5')
bucket = conn.get_bucket('music-emotions')
i = 0
for key in bucket.list():
    genre = key.name.split(str="/",num=1)[0]
    name = key.name.split(str="/", num=1)[1]
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

    print log("Creating song #"+i+" : "+name)
    song = Song(name=name, genre=genre, audio_file=key.name)
    song.save()
    i += 1
