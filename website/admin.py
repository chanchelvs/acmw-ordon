from django.contrib import admin
from .models import  *
# Register your models here.
admin.site.register(Hospital)
admin.site.register(Donor)
admin.site.register(Location)
admin.site.register(Campaign)
admin.site.register(Organ)
admin.site.register(Fund)
admin.site.register(Notification)