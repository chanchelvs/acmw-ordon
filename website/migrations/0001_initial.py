# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-02 13:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_fund', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('acc_no', models.CharField(max_length=20)),
                ('ifsc_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_patient', models.BooleanField(default=False)),
                ('dob', models.DateField(null=True)),
                ('blood_group', models.CharField(choices=[('ave', 'A+ve'), ('a-ve', 'A-ve'), ('bve', 'B+ve'), ('b-ve', 'B-ve'), ('ove', 'O+ve'), ('o-ve', 'O-ve'), ('abve', 'AB+ve'), ('ab-ve', 'AB-ve')], max_length=20)),
                ('is_alive', models.BooleanField(default=True)),
                ('aadhar_no', models.IntegerField()),
                ('phone_no', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Campaign')),
                ('funded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Donor')),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=500)),
                ('type', models.CharField(max_length=200)),
                ('priority', models.IntegerField(default=1)),
                ('is_read', models.BooleanField(default=False)),
                ('url', models.CharField(blank=True, max_length=1000, null=True)),
                ('frm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='frm_user', to=settings.AUTH_USER_MODEL)),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('heart', 'Heart'), ('lungs', 'Lungs'), ('kidney', 'Kidney'), ('liver', 'Liver'), ('blood', 'Blood')], max_length=100)),
                ('blood_group', models.CharField(choices=[('ave', 'A+ve'), ('a-ve', 'A-ve'), ('bve', 'B+ve'), ('b-ve', 'B-ve'), ('ove', 'O+ve'), ('o-ve', 'O-ve'), ('abve', 'AB+ve'), ('ab-ve', 'AB-ve')], max_length=20)),
                ('is_available', models.BooleanField(default=True)),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organ_donor', to='website.Donor')),
                ('organ_hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Hospital')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organ_receiver', to='website.Donor')),
            ],
        ),
        migrations.AddField(
            model_name='hospital',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Location'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donor',
            name='donor_hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Hospital'),
        ),
        migrations.AddField(
            model_name='donor',
            name='donor_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Location'),
        ),
        migrations.AddField(
            model_name='donor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campaign',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Donor'),
        ),
    ]
