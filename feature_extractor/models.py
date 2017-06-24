from __future__ import unicode_literals

from django.db import models


# Create your models here.
class SongFeatureSet(models.Model):
    """
        This models contains all the possible features that can be used for
        training a model on emotion classification.
    """
