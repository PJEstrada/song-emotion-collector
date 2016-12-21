# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext as _n
from django.core.management.base import BaseCommand, CommandError
from django.contrib.staticfiles.templatetags.staticfiles import static


class Command(BaseCommand):
    help = "Sends emails to every user with a pending PasswordRetrievalEvent token."

    def handle(self, *args, **kwargs):
        indir = '/home/des/test'
        for root, dirs, filenames in os.walk(indir):
            for f in filenames:
                print(f)
                path = indir + f
                print path
                # log = open(path, 'r')
                # Create Song object.
                # With the correct media configuration it should be automatically uploaded to S3
                return
