# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20170116_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='s3_path',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]