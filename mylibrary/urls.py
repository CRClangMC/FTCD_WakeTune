# -*-coding:utf8-*-
"""mylibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.dinco, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path as url
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from show import views as show_views 

 
urlpatterns = [     
    url(r'^$', show_views.login),
    url(r'^login/$', show_views.login, name='login'),
    url(r'^musictg/$', show_views.musictg, name='musictg'),
    url(r'^access/$', show_views.access, name='access'),
    url(r'^accessph/$', show_views.accessph, name='accessph'),
    url(r'^accessph2/$', show_views.accessph2, name='accessph2'),
    url(r'^pwdset/$', show_views.pwdset, name='pwdset'),
    url(r'^admlogin/$', show_views.admlogin, name='admlogin'),
    url(r'^admins/$', show_views.admins, name='admins'),
    url(r'^adminset/$', show_views.adminset, name='adminset'),
    url(r'^pwdset1/$', show_views.pwdset1, name='pwdset1'),
    url(r'^phblock/$', show_views.phblock, name='phblock'),
    url(r'^adminall/$', show_views.adminall, name='adminall'),
    # DEBUG = False 时使用
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}, name='static'),
]



