import xmltodict
import pycurl
import io
import urllib



"""
Diccionarios para el parser de aparcamientos
"""


KeyItemsSecond = [
            'NOMBRE-VIA', 'CLASE-VIAL', 'LOCALIDAD','PROVINCIA',
            'CODIGO-POSTAL', 'BARRIO', 'DISTRITO', 'LATITUD', 'LONGITUD',
            'TELEFONO', 'EMAIL',
    ]   #campos que voy a guardar
KeyItemsFirst = [
            'ID-ENTIDAD', 'NOMBRE', 'DESCRIPCION', 'ACCESIBILIDAD',
            'CONTENT-URL', 'LOCALIZACION', 'DATOSCONTACTOS',
            'TELEFONO', 'EMAIL',
    ]
"""
Diccionario de conversión de nombre de campo del XML a models
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

URL_data = 'http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full'


"""
Método que convierte una URL de un XML en un diccionario parseable
"""

def get_dict_from_url():


    file_sofia = urllib.request.urlopen(URL_data)
    res_dict = file_sofia.read()
    res_dict = xmltodict.parse(res_dict)

    return res_dict


# res['Contenidos']['contenido'][0]['atributos']['atributo'][7]

#from aparcamientos.helpers import *

"""
Método para aquellos nodos del árbol XML que tuvieran mayor profundidad
"""
def parse_deeper(loc_field, park_number):
    #para los elementos que tienen más atributos
    LocDict = {}
    for indexLocal, _ in enumerate(loc_field):
        try:
            campo_localizacion = loc_field[indexLocal]['@nombre']
        except KeyError:
            continue
        if campo_localizacion in KeyItemsSecond:
            LocDict[campo_localizacion] = loc_field[indexLocal]['#text']

    return LocDict

"""
Método que parsea un aparcamiento (nodo del árbol XML). Devuelve un diccionario {propiedad: valor}
"""
def parse_park(park_item):
    dict_park = {}   # vacío el diccionario porque si no sobreescribe lo mismo y guarda lo anterior
    for index, item in enumerate(park_item):
        aux_dict_park = {}
        campo = park_item[index]['@nombre']
        if campo == 'LOCALIZACION' or campo == 'DATOSCONTACTOS':    #tengo que profundizar en el árbol
            try:                                                    # Falla porque no todos los aparcamientos tienen datos de contacto
                aux_dict_park = parse_deeper(park_item[index]['atributo'], index)
            except KeyError:
                pass
        elif campo in KeyItemsFirst:                # es dato básico
            aux_dict_park = {campo: park_item[index]['#text']}

        dict_park.update(aux_dict_park)     #d.update(dict2)
    return dict_park


def migrate_park_data():

    res = get_dict_from_url()
    
    """
    Parsea un XML. Devuelve una lista de diccionarios. Cada índice es un aparcamiento
    """

    list_park = []       #Lista de diccionarios. Cada índice de la lista es un aparcamiento y contiene su descripción
    
    list_contenido = res['Contenidos']['contenido'] #267 aparcamientos

    for  park in list_contenido:
        list_park.append(parse_park(park['atributos']['atributo']))

    return list_park











    """

    list_contenido = res['Contenidos']['contenido']

    i=1
    for contenido in list_contenido:
        atributos = contenido['atributos']

        number = atributos['atributo'][0]['#text']
        nombre = atributos['atributo'][1]['#text']
        descripcion = atributos['atributo'][2]['#text']
        accesible = atributos['atributo'][3]['#text']
        url = atributos['atributo'][4]['#text']
        #via = atributos['atributo'][5]['atributo'][0]['#text']
        #localidad = atributos['@nombre'][5]['atributo'][1]['#text']
        #provincia = atributos['atributo'][5]['atributo'][2]['#text']
        #codigo_postal = atributos['atributo'][5]['atributo'][3]['#text']
        #barrio = atributos['atributo'][5]['atributo'][4]['#text']
        #distrito = atributos['atributo'][5]['atributo'][5]['#text']
        #latitud = atributos['atributo'][5]['atributo'][6]['#text']
        #telefono = atributos['atributo'][6]['atributo'][0]['#text']
        #email =atributos['atributo'][6]['atributo'][0]['#text']
        #print ( "aparcamiento" number, nombre, descripcion, accesible, url, via, localidad, provincia, codigo_postal, barrio, distrito, latitud, telefono, email "\n")
        i=i+1
    """