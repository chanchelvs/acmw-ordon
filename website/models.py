from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


def get_choices(options):
    return zip([slugify(x) for x in options], options)

blood_group_choices = get_choices(['A+ve', 'A-ve', 'B+ve', 'B-ve', 'O+ve', 'O-ve', 'AB+ve', 'AB-ve'])
organ_choices = get_choices(['Heart', 'Lungs', 'Kidney', 'Liver', 'Blood'])
# create your models here.

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.address)[:10] + str(self.latitude)[:3]+","+str(self.longitude)[:3]
        # return str(self.address)

class Hospital(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length = 100)
    location = models.ForeignKey(Location, null = True, blank = True)
    type = models.CharField(max_length = 100)
    def __str__(self):
        return str(self.name) + ", " +  str(self.user.username)

class Donor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length = 100)
    is_patient = models.BooleanField(default = False)
    donor_location = models.ForeignKey(Location, null = True, blank = True)
    donor_hospital = models.ForeignKey(Hospital, null = True)
    dob = models.DateField(null =  True)
    blood_group = models.CharField(max_length = 20, choices = blood_group_choices)
    is_alive = models.BooleanField(default = True)
    aadhar_no = models.IntegerField()
    phone_no = models.CharField(max_length = 20)
    def __str__(self):
        return str(self.name) + ", " + str(self.user.username)


class Organ(models.Model):
    type = models.CharField(max_length = 100, choices = organ_choices)
    donor = models.ForeignKey(Donor, null =  True, blank = True, related_name='organ_donor')
    receiver = models.ForeignKey(Donor, null = True, blank = True, related_name='organ_receiver')
    blood_group = models.CharField(max_length = 20, choices = blood_group_choices)
    is_available = models.BooleanField(default =  True)
    organ_hospital = models.ForeignKey(Hospital, null = True, blank = True)
    def __str__(self):
        return str(self.type) + ", " + str(self.blood_group) + ", " +  str(self.donor.user.username)

class Campaign(models.Model):
    posted_by = models.ForeignKey(Donor)
    target_fund = models.IntegerField(default = 0)
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 1000)
    acc_no = models.CharField(max_length = 20)
    ifsc_code = models.CharField(max_length = 20)
    def __str(self):
        return str(self.target_fund) + ", " + str(self.posted_by) + ", " + str(self.title)


class Notification(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length = 500)
    type = models.CharField(max_length = 200)
    to = models.ForeignKey(User, null = True, related_name='to_user')
    frm = models.ForeignKey(User, null = True, blank = True, related_name='frm_user')
    priority = models.IntegerField(default = 1)
    is_read = models.BooleanField(default = False)
    url = models.CharField(max_length = 1000, null = True, blank = True)
    def __str__(self):
        return str(self.title) + ", " + str(self.to)

class Fund(models.Model):
    campaign = models.ForeignKey(Campaign)
    amount = models.IntegerField(default = 0)
    funded_by = models.ForeignKey(Donor)
    def __str__(self):
        return str(self.amount) + ", " + str(self.funded_by) + ", "+ str(self.campaign)
