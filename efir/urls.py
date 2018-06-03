"""efir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from efirapp import views
from django.conf.urls import  url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.home),
    path('record',views.record),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    url('upload/(?P<aadhaar_id>\d+)/(?P<otp>\d+)', views.complain_file),
    path('upload/login', views.complain_login),
    path('track',views.track_login),
    url('track/(?P<fir_id>\d+)',views.status),
    url('search', views.search, name='search'),
    url('status/(?P<fir_id>\d+)/update/$', views.statusupdateview.as_view()),
    url('aadhar/(?P<aadhaar_id>\d+)', views.aadhar)
]
