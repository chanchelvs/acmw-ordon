# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-02 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20171002_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
        migrations.AddField(
            model_name='notification',
            name='name',
            field=models.CharField(default='hello', max_length=200),
            preserve_default=False,
        ),
    ]
