# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20161214_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='email',
            field=models.EmailField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
