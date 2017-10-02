from django.db.models import QuerySet
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from .models import *
import json

# Create your views here.
def faq(request):
    return render_to_response("faq.html")

def firstaid(request):
    return render_to_response("firstaid.html")

def welcome(request):
    hospitals_from_db =  Hospital.objects.all()
    hospitals = []
    requirements = []
    for hospital in hospitals_from_db:
        hospitals.append({"name": hospital.name,
                          "latitude": hospital.location.latitude,
                          "longitude": hospital.location.longitude})
        organs_in_hospital = Organ.objects.filter(organ_hospital = hospital).order_by('type')
        requirement = ""
        total_organs_count = len(organs_in_hospital)
        cur_count = 0
        for i in range(total_organs_count):
            if(i == total_organs_count - 1 or  organs_in_hospital[i].type != organs_in_hospital[i+1].type):
                cur_count += 1
                requirement += ("<li>" + str(organs_in_hospital[i].type) + " - " + str(cur_count) + "</li>")
                cur_count = 0
            else:
                cur_count += 1
        requirements.append(requirement)

    hospitals_json = json.dumps(hospitals)
    requirements_json = json.dumps(requirements)
    data = {'hospitals': hospitals_json,'requirements': requirements_json}
    return render(request, "welcome.html", data)

@login_required
def home(request):
    return render_to_response("home.html")

