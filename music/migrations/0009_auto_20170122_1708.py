# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-22 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_song_s3_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='gender',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], default=('Masculino', 'Masculino'), max_length=50),
        ),
    ]
