"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.static import *
from project import settings
from aparcamientos import views, urls as urls_aparcamientos

urlpatterns = [
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL}),
    #url(r'^prueba$', "aparcamientos.views.Prueba", name='Principal'),
    # Admin site
    url(r'^admin/', include(admin.site.urls)),
    # /
    url(r'^$', views.Principal, name='Principal'),


    #aparcamiento/id
    url(r'^aparcamientos/', include(urls_aparcamientos)),

    #pagina usuario
    url(r'^usuario/$', views.personal),

    #pagina personalizar usuario
    url(r'^usuario/personaliza/$', views.cambio_estilo),

    #pagina xml de un usuario
    url(r'^usuario/xml/$', views.user_xml),

    #página about
    url(r'^about/$', views.about, name='about'),

    #Login
    url(r'^login/$', views.Login, name='Login de un usuario'),

    #logout --- no hace bien el logout
    url(r'^logout/$', logout, {'next_page': '/'}),

]
