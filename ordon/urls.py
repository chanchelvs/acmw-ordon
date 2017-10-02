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
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]
