"""pyproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from nurtureApp import views

urlpatterns = [
    url(r'^admin/advisor', views.CreateAdvisor),
    url(r'^user/register', views.CreateUser),
    url(r'^user/login', views.LoginUser),
    url(r'^user/(?P<user_id>\d+)/advisor/(?P<advisor_id>\d+)', views.BookCall),
    url(r'^user/(?P<user_id>\d+)/advisor/booking', views.ListBooking),
    url(r'^user/(?P<user_id>\d+)/advisor', views.ListAdvisor),
]
