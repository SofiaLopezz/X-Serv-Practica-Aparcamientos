from django.conf.urls import url
from project import settings
from aparcamientos import views

urlpatterns = [
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL}),
    url(r'^$', views.aparcamientos_todos, name='aparcamiento_todos'),
    url(r'^active$', views.active_available_park, name='active_availables'),
    url(r'^disactive$', views.disactive_available_park, name='disactive_availables'),
    url(r'(?P<id>\d+)$', views.aparcamiento_detalle, name='aparcamiento_detalle'),
    url(r'(?P<id>\d+)/add$', views.add_comment, name='add_comment'),
    url(r'(?P<id>\d+)/addfavorito$', views.add_favorito, name='addfavorito'),
	url(r'(?P<id>\d+)/removefavorito$', views.remove_favorito, name='removefavorito'),

    url(r'^comunidad$', views.comunidad, name='comunidad'),
    url(r'comunidad/(?P<username>\w+)$', views.profileguay, name='paginausuarioscomunidad'),



]
