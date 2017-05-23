import sys

from django.shortcuts import render, render_to_response, redirect
from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate, login
from django.template import loader
from django.core import serializers
from aparcamientos.helpers import migrate_park_data
from .models import Usuario, Aparcamiento, Comentario, Pagina 

from django.contrib.auth.models import User as user
from django.contrib.auth.decorators import login_required



""""
Parse
"""
Estandar_to_ModelDict = {
            'ID-ENTIDAD': 'number',
            'NOMBRE': 'nombre',
            'DESCRIPCION' : 'descripcion',
            'ACCESIBILIDAD' : 'accesible',
            'CONTENT-URL' : 'url',
            'NOMBRE-VIA' : 'via',
            'LOCALIDAD' : 'localidad',
            'PROVINCIA' : 'provincia',
            'CODIGO-POSTAL' : 'codigo_postal',
            'BARRIO' : 'barrio',
            'DISTRITO' : 'distrito',
            'LATITUD' : 'latitud',
            'LONGITUD' : 'longitud',
            'TELEFONO' : 'telefono',
            'EMAIL' : 'email',
}


"""
Dado un parsed, actualiza la base de datos de aparcamientos
"""
def update_data_base(parsed_list):
    print(parsed_list)
    #Guardamos los aparcamientos
    for Park in parsed_list:
        dicc = {}
        print("Updating 'Aparcamiento' data base...")
        model_dict_create = {}   # diccionario de propiedad: valor, con el nombre dado en el Modelo Django (aparcamiento)
        for property in Park:
            try:
                model_property = Estandar_to_ModelDict[property]
                if property == 'ACCESIBILIDAD':
                    if Park[property] == '1':
                        model_dict_create['accesible'] = True
                    else:
                        model_dict_create['accesible'] = False

                else :
                    model_dict_create[model_property] = Park[property]
            except KeyError:
                pass
        try:
            #Comprobación para no crear 20 veces el mismo aparcamiento. Si por alguna razón ya existe, pasamos sin más
            Aparcamiento.objects.get(number = model_dict_create['number'])
            continue
        except Aparcamiento.DoesNotExist:
            Aparcamiento.objects.create(**model_dict_create)
            pass

    return None


def check_data_base():
    if Aparcamiento.objects.all().count() == 0:
        park_data_xml = migrate_park_data()
        update_data_base(park_data_xml)
        print('actualizada')
    return None







"""
Página principal del sitio: devuelvo el banner, formulario de login o mensaje de bienvenida.
Devuelvo el menu horizontal y vertical y la lista de los 5 aparcamientos con más comentarios
"""

@csrf_exempt
def Principal(request):
  context = {}
  if request.method != 'GET':
      raise Exception("405")

  if 'only_active' in request.session.keys() and request.session['only_active']:
    top_aparcamientos = Aparcamiento.objects.filter(accesible=True).annotate(num_coment = Count('comentarios')).order_by('num_coment')
    accesibilidad = True
  else:
    accesibilidad = False
  # Dame todos los aparcamientos. Dame el contador de comentarios de cada uno. Ordenalos por numero de comentarios. Excluye los que no tengan comentarios.
    top_aparcamientos = Aparcamiento.objects.annotate(num_coment = Count('comentarios')).exclude(num_coment = 0)[:5]
    #aparcamiento = Aparcamiento.objects.annotate(num_coment = Count('comentarios')).exclude(num_coment = 0)[:5]


    
  
  #top_aparcamientos = Comentario.objects.all().order_by('-aparcamiento__id').unique()[:5]
  pagina_list = Pagina.objects.all()       

  context['inicio'] = 'active'
  context['top_aparcamientos'] = top_aparcamientos
  context['pagina_list'] = pagina_list
  context['user'] = request.user
  context['accesibilidad'] = accesibilidad

  return render_to_response('index.html', context)

@csrf_exempt
def active_available_park(request):
  request.session['only_active'] = True
  return redirect('/')
  

@csrf_exempt
def disactive_available_park(request):
  request.session['only_active'] = False
  return redirect('/')


"""
Cuando recibo un LOGIN: si el método es POST, compruebo si el nick y password coinciden con la base de datos. Si lo hacen, debería autenticar al usuario, usar
el login ese de las diapos, no se como. Si falla, no lo autentico. En cualquier caso, aunque el método sea invalido, redireccion a la pagina principal
"""
@csrf_exempt
def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      

      if not hasattr(user, 'usuario'):

        usuario = Usuario(usuario=user)
        usuario.save()


      login(request, user)

    else:
        # Return an 'invalid login' error message.
        print('fallo')
    return redirect('/')

"""
Página con la info de un determinado aparcamiento
"""

@csrf_exempt
def aparcamiento_detalle(request, id):
    context = {}
    context['user'] = request.user

    aparcamiento = Aparcamiento.objects.filter(pk=id).first()
    comentarios= Comentario.objects.filter(aparcamiento__pk=id).order_by("fecha")
    if aparcamiento:
      
      context['park'] = 'active'
      context['aparcamiento'] = aparcamiento
      context['comentarios'] = comentarios

      # crear el nuevo comentario
    return render_to_response('aparcamiento_id.html', context)

    #raise Exception(id)

@csrf_exempt
def add_comment(request, id):
  if request.method =='POST':
      aparcamiento = Aparcamiento.objects.filter(pk=id).first()
      texto = request.POST['comentario']
      usuario = request.user.usuario

      
      Comentario.objects.create(
          usuario = usuario,
          texto = texto,
          aparcamiento = aparcamiento,
      )
  return redirect("/aparcamientos/{}".format(id))


"""
Página about del sitio
"""
@csrf_exempt
def about(request):
    context = { }
    context['about'] = 'active'
    context['user'] = request.user

  
    return render_to_response('about.html', context)

"""
Página con la info básica de todos los aparcamientos. Si el método es GET, devuelvo todos los aparcamientos.
Si es POST, filtro el distrito
"""
@csrf_exempt
def aparcamientos_todos(request):
    context = {}

    context['user'] = request.user
    context['park'] = 'active'

    check_data_base()

    if request.method == 'GET':
        # aparcamiento = Aparcamiento.objects.all()
      
        # Dame todos los aparcamientos. Dame el contador de comentarios de cada uno. Ordenalos por numero de comentarios. Excluye los que no tengan comentarios.
        aparcamiento = Aparcamiento.objects.annotate(
            num_coment = Count('comentarios')
        )
        if request.user.is_authenticated:
          for park in aparcamiento:
              park.favorito = len(park.usuarios.filter(usuario=request.user)) > 0
               
        context['aparcamientos'] = aparcamiento

    elif request.method == 'POST':
        #para filtrar por distrito
        filter_value = request.POST['filtro_value']
        filter_name = request.POST['filtro_name']
        message = 'Mostrando aparcamientos por: ' + filter_name
        if filter_name =='':
            aparcamiento = Aparcamiento.objects.all()
        else:
          aparcamiento = Aparcamiento.objects.filter(**{filter_name: filter_value})

          context['aparcamientos'] = aparcamiento
          context['message'] = message


    return render_to_response('aparcamientos.html', context)


"""
Cuando recibo un LOGIN: si el método es POST, compruebo si el nick y password coinciden con la base de datos. Si lo hacen, debería autenticar al usuario, usar
el login ese de las diapos, no se como. Si falla, no lo autentico. En cualquier caso, aunque el método sea invalido, redireccion a la pagina principal
"""
def add_favorito(request, id):
    user=request.user
    if user:
        aparcamiento = Aparcamiento.objects.filter(pk=id).first()
        if aparcamiento:

          aparcamiento.usuarios.add(user.usuario)

    return redirect('/aparcamientos/')


def remove_favorito(request, id):
    user=request.user
    if user:
        aparcamiento = Aparcamiento.objects.filter(pk=id).first()
        if aparcamiento:

          aparcamiento.usuarios.remove(user.usuario)
          
    return redirect('/aparcamientos/')

"""
Página de un usuario determinado: mostrar aparcamientos seleccionados por ese usuario, de 5 en 5
Comprobar si el usuario existe. Si existe, comprobar si tiene un estilo asociado. Si lo tiene, devolverle el estilo. Si no, le ponemos el
estandar (negro,1em)
"""
@login_required
@csrf_exempt
def personal(request):
  context = {}

  usuario = request.user.usuario
  user = request.user
  context['user'] = user
  context['usuario'] = usuario
  context['personal'] = 'active'

  aparcamientos = None
  if user:
    # Para niños
    aparcamiento = Aparcamiento.objects.filter(usuarios__usuario=user)
    # Para los mayores
    aparcamientos = user.usuario.aparcamientos.all()




  context['aparcamientos'] = aparcamientos

  if request.method == 'GET':
    pass

  return render_to_response('profile.html', context)
 

"""
Método que devuelve el objecto 'Estilo' del usuario solicitante.
Busca en la base, si existe el usuario, lo devuelve. Si no, crea uno nuevo con los parámetros por defecto
"""

@login_required
@csrf_exempt
def cambio_estilo(request):
    if request.method =='POST':
      user = request.user

      usuario = user.usuario


      background_color_default = '#f5f5f5'
      if 'color' in request.POST:
        background_color_default = request.POST['color']

      size_default = '80' # en porcentaje
      if 'size' in request.POST:
        size_default = request.POST['size']

      titulo = ""
      if 'nombre_pagina' in request.POST:
        titulo = request.POST['nombre_pagina']
      
      usuario.size = size_default
      usuario.color = background_color_default
      usuario.nombre_pagina = titulo
      usuario.save()


    
    return redirect("/usuario/")


"""
Página con el XML de un usuario determinado
"""

def user_xml(request):
    context = {}

    user_serialized_xml = serializers.serialize("xml", Usuario.objects.all())
    context['user_serialized_xml'] = user_serialized_xml
    return render_to_response('profile_xml.html', context)


"""
Página de la comunidad
"""

def comunidad(request):
  context = {}
  context['user']=request.user
  context['comunidad'] = Usuario.objects.all().annotate(num_park=Count('aparcamientos'))

  return render_to_response('comunidad.html', context)


"""
Página de un usuario 
"""

def profileguay(request, username):
  context = {}
  context['user']=request.user
  usuariodelquequierolapagina =  Usuario.objects.filter(usuario__username=username).first()
  aparcamientos = usuariodelquequierolapagina.aparcamientos.all()

  context['usuario'] = usuariodelquequierolapagina
  context['aparcamientos'] = aparcamientos

  context['comunidad'] = Usuario.objects.all().annotate(num_park=Count('aparcamientos'))

  return render_to_response('profileguay.html', context)