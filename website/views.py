from django.db.models import QuerySet
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .utilities import *
import json

# Create your views here.
def faq(request):
    return render_to_response("faq.html")

def firstaid(request):
    return render_to_response("aid.html")

def welcome(request):
    hospitals_from_db =  Hospital.objects.all()
    hospitals = []
    requirements = []
    for hospital in hospitals_from_db:
        hospitals.append({"name": hospital.name,
                          "latitude": hospital.location.latitude,
                          "longitude": hospital.location.longitude})
        organs_in_hospital = OrganRequired.objects.filter(organ_hospital = hospital).order_by('type')
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
    try:
        hospital = Hospital.objects.get(user = request.user)
        notifications = Notification.objects.filter(is_read=False, to = request.user)
        return render(request, "home.html",{'notifs':notifications,'notifcount':len(notifications)})
    except:
        pass
    notifications = Notification.objects.filter( to=request.user)
    tempnotif = notifications.values()
    for i in notifications:
        i.is_read =True
        i.save()
    return render(request, "donor_home.html",{'notifs':notifications,'notifcount':len(notifications)})

#hospital views
@login_required
def new_patient(request):
    if(request.method=='POST'):
        username = (request.POST.get('username'))
        password1 = (request.POST.get('password1'))
        password2 = (request.POST.get('password2'))
        name = (request.POST.get('name'))
        email = (request.POST.get('email'))
        phone = (request.POST.get('phone'))
        blood_group = (request.POST.get('blood_group'))
        aadhar_no = (request.POST.get('aadhar_no'))
        dob = (request.POST.get('dob'))
        photo = (request.FILES['photo'])
        if(password1==password2):
            try:
                user = User.objects.get(username=username)
                return render(request,'new_patient.html',{'message':'Select a different username'})
            except:
                user = User.objects.create_user(username, email, password1)
            user = User.objects.get(username=username)
            handle_uploaded_file(photo,username+'_.jpg')
            hospital = Hospital.objects.get(user=request.user)
            donor = Donor(user = user,
                          name=name,
                          phone_no=phone,
                          blood_group=blood_group,
                          dob = dob,
                          aadhar_no = aadhar_no,
                          donor_hospital = hospital,
                          is_patient=True,
                          photo=username+'_.jpg')
            donor.save()
            return redirect('/list_patients/')
        else:
            return render(request,'new_patient.html',{'message':'Passwords does not match'})
    else:
        return render(request,'new_patient.html')


@login_required
def list_patients(request):
    hospital = Hospital.objects.get(user=request.user)
    patients = []
    if 'search' in request.GET:
        query = request.GET.get('q')
        query = query.split(' ')[0].lower()
        patients = Donor.objects.filter(is_patient=True, donor_hospital=hospital,name__contains=query)
    else:
        patients = Donor.objects.filter(is_patient=True, donor_hospital=hospital)

    data = {'patients':patients}
    #print(data)
    return render(request,"list_patients.html",data)


@login_required
def list_donors(request):
    hospital = Hospital.objects.get(user=request.user)
    donors = Donor.objects.filter(is_patient=False, donor_hospital =hospital)
    data = {'donors':donors}
    #print(data)
    return render(request,"list_donors.html",data)

@login_required(login_url='/login/')
def delete_patient(request):
    patient_pk = request.GET.get('id')
    try:
        patient = Donor.objects.get(pk=patient_pk)
        patient.delete()
        return redirect("/list_patients/")
    except:
        return redirect("/list_patients/")

@login_required(login_url='/login/')
def delete_donor(request):
    donor_pk = request.GET.get('id')
    try:
        donor = Donor.objects.get(pk=donor_pk)
        donor.delete()
        return redirect("/list_donors/")
    except:
        return redirect("/list_donors/")

@login_required
def blood_details(request):
    if request.method == 'POST':
        group = request.POST.get('blood_group')
        quantity = request.POST.get('quantity')
        for i in range(int(quantity)):
            blood = Organ(type='Blood', blood_group = group)
            blood.save()
    bloods = Organ.objects.filter(type='Blood').order_by('blood_group')
    bloods_a = []
    total_organs_count = len(bloods)
    cur_count = 0
    for i in range(total_organs_count):
        if (i == total_organs_count - 1 or bloods[i].blood_group != bloods[i + 1].blood_group):
            cur_count += 1
            bloods_a.append({"blood_group":bloods[i].blood_group, "count":cur_count})
            cur_count = 0
        else:
            cur_count += 1
    data = {'bloods':bloods_a}
    print data
    return render(request,"blood_details.html",data)

@login_required
def organ_required(request):
    organs = OrganRequired.objects.exclude(type='Blood').order_by('type')
    organs_a = []
    total_organs_count = len(organs)
    cur_count = 0
    for i in range(total_organs_count):
        organs_a.append({"type":organs[i].type,"blood_group":organs[i].blood_group,"patient":organs[i].patient.user.username})
    data = {'organs':organs_a}
    print data
    return render(request,"organ_details.html",data)

@login_required
def new_organ_require(request):
    if request.method == 'POST':
        patient_pk = request.POST.get('patient')
        type = request.POST.get('organ_type')
        blood_group = request.POST.get('blood_group')
        priority = request.POST.get('priority')
        patient = Donor.objects.get(pk = patient_pk)
        organ_required = OrganRequired(type = type,
                                       patient = patient,
                                       blood_group = blood_group,
                                       organ_hospital = patient.donor_hospital)
        organ_required.save()
        return redirect('/organ_required/')
    data = {'patients':Donor.objects.filter(is_patient=True,donor_hospital__user=request.user),'organs':organ_choices}
    return  render(request,"new_organ_require.html",data)

@login_required
def transplant_history(request):
    organs = Organ.objects.exclude(type='Blood',receiver__isnull=True).order_by('type')
    organs_a = []
    total_organs_count = len(organs)
    cur_count = 0
    # for i in range(total_organs_count):
    #     organs_a.append({"type":organs[i].type,"blood_group":organs[i].blood_group,"donor":organs[i].donor.name,"receiver":organs[i].receiver.name})
    data = {'organs':organs}
    return render(request,"transplant_history.html",data)

#notification things

@login_required
def new_notification(request):
    if request.method == 'POST':
        user_pk = request.POST.get('user')
        title = request.POST.get('title')
        content = request.POST.get('content')
        notification = Notification(to = User.objects.get(pk = user_pk),
                                    frm = request.user,
                                    name = title,
                                    text = content)
        notification.save()
    donors = Donor.objects.filter(donor_hospital__user = request.user)
    data = {'patients':donors}
    return render(request,"new_notification.html",data)

@login_required
def list_notifications(request):
    notifs = Notification.objects.filter(to = request.user)
    data = {'notifs':notifs}
    for notif in notifs:
        notif.is_read = True
        notif.save()
    return render(request,"list_notifications.html",data)


@login_required
def report_death(request):
    if request.method == 'POST':
        req = request.POST
        print req
        person = req.get('user')
        user = User.objects.get(pk = person)
        patient = Donor.objects.get(user = user)
        patient.is_alive = False
        patient.save()
        for i in organ_choices:
            print i, req.get(i[1])
            if(req.get(i[1]) == 'on'):
                organ = Organ(type=i[1],
                               donor=patient,
                               blood_group=patient.blood_group,
                               organ_hospital=patient.donor_hospital)
                organ.save()
        give_notification(request)

    donors = Donor.objects.filter(donor_hospital__user=request.user)
    data = {'patients': donors}
    return render(request,"report_death.html",data)

@login_required
def donor_registration(request):
    if(request.method=='POST'):
        username = (request.POST.get('username'))
        password1 = (request.POST.get('password1'))
        password2 = (request.POST.get('password2'))
        name = (request.POST.get('name'))
        email = (request.POST.get('email'))
        phone = (request.POST.get('phone'))
        blood_group = (request.POST.get('blood_group'))
        aadhar_no = (request.POST.get('aadhar_no'))
        dob = (request.POST.get('dob'))
        photo = (request.FILES['photo'])
        if(password1==password2):
            try:
                user = User.objects.get(username=username)
                return render(request,'donor_reg.html',{'message':'Select a different username'})
            except:
                user = User.objects.create_user(username, email, password1)
            user = User.objects.get(username=username)
            handle_uploaded_file(photo,username+'_.jpg')
            donor = Donor(user = user,
                          name=name,
                          phone_no=phone,
                          blood_group=blood_group,
                          dob = dob,
                          aadhar_no = aadhar_no,
                          photo=username+'_.jpg')
            donor.save()
            return redirect('/list_donors/')
        else:
            return render(request,'donor_reg.html',{'message':'Passwords does not match'}) 
    else:
        return render(request,'donor_reg.html')


def give_notification(request):
    organs_available = Organ.objects.exclude(type='Blood').order_by('type')
    organs_required = OrganRequired.objects.exclude(type='Blood').order_by('type')
    for organ_required in organs_required:
        for organ_available in organs_available:
            if(organ_required.type == organ_available.type and organ_required.blood_group == organ_available.blood_group):
                if len(OrganRequired.objects.filter(pk = organ_required.pk)) > 0:
                    receiver = organ_required.patient
                    organ_available.receiver = receiver
                    organ_available.is_available = False
                    organ_available.save()
                    notification = Notification(frm = request.user,
                                                to = receiver.user,
                                                name = 'Received Organ Transplant!',
                                                text='Your request for a organ transplant of ' + str(organ_required.type) + ' has been met, please contact your home hospital')
                    notification.save()
                    hospital_notification = Notification(frm = request.user,
                                                         to = receiver.donor_hospital.user,
                                                         name = 'New Organ transplant ',
                                                         text = 'New organ transplant pending for patient ' +
                                                                receiver.name + ' (Ph no : ' + receiver.phone_no +
                                                                ' )' + ' for ' + organ_required.type + '. please make necessary arrangements')
                    hospital_notification.save()
                    organ_required.delete()

