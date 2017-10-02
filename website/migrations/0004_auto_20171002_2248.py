# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-02 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_organrequired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organ',
            name='type',
            field=models.CharField(choices=[('heart', 'Heart'), ('lungs', 'Lungs'), ('kidney', 'Kidney'), ('liver', 'Liver'), ('eyes', 'Eyes'), ('blood', 'Blood')], max_length=100),
        ),
        migrations.AlterField(
            model_name='organrequired',
            name='type',
            field=models.CharField(choices=[('heart', 'Heart'), ('lungs', 'Lungs'), ('kidney', 'Kidney'), ('liver', 'Liver'), ('eyes', 'Eyes'), ('blood', 'Blood')], max_length=100),
        ),
    ]
