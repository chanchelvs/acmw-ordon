# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-02 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='photo',
            field=models.CharField(default='ic_hospital.png', max_length=200),
            preserve_default=False,
        ),
    ]