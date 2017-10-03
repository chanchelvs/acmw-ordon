from django.conf.urls import include, url
from django.contrib import admin
from website import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    # Examples:
    # url(r'^$', 'ordon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.welcome, name='welcome'),
    url(r'^home/$', views.home, name='home'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^firstaid/$', views.firstaid, name='firstaid'),
    #hospital urls
    url(r'^new_patient/$', views.new_patient, name='new_patient'),
    url(r'^list_patients/$', views.list_patients, name='list_patients'),
    url(r'^delete_patient/$', views.delete_patient, name='delete_patient'),

    # donor urls
    url(r'^new_donor/$', views.donor_registration, name='new_donor'),
    url(r'^list_donors/$', views.list_donors, name='list_donors'),
    url(r'^delete_donor/$', views.delete_donor, name='delete_donor'),

    #organ urls
    url(r'^blood_details/$', views.blood_details, name='blood_details'),
    url(r'^organ_required/$', views.organ_required, name='organ_required'),
    url(r'^new_organ_require/$', views.new_organ_require, name='new_organ_require'),
    url(r'^transplant_history/$', views.transplant_history, name='transplant_history'),

    # notification stuff
    url(r'^new_notification/$', views.new_notification, name='new_notification'),
    url(r'^list_notification/$', views.list_notifications, name='list_notifications'),
    url(r'^report_death/$', views.report_death, name='report_deathv'),


    # admin and login urls
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]
