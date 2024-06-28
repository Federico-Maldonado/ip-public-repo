# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user
#import de la libreria passlib para el login encriptacion y desencriptacion
from passlib.hash import django_pbkdf2_sha256 


def getAllImages(input=None):
    # obtiene un listado de imágenes desde transport.py y lo guarda en un json_collection.
    # ¡OJO! el parámetro 'input' indica si se debe buscar por un valor introducido en el buscador.
    

    json_collection = []
    json_collection = transport.getAllImages(input=None)
    images = []
    i=0
    #revisar.
    for x in json_collection:
        images.append(mapper.fromRequestIntoNASACard(x)) 


    # recorre el listado de objetos JSON, lo transforma en una NASACard y lo agrega en el listado de images. Ayuda: ver mapper.py.

    return images


def getImagesBySearchInputLike(input):
    return getAllImages(input)


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):

    fav=mapper.fromTemplateIntoNASACard(request)
    user = get_user(request)
     # transformamos un request del template en una NASACard.
    fav.user = user # le seteamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.


# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        
        favourite_list = [] # buscamos desde el repositorio TODOS los favoritos del usuario (variable 'user').
        favourite_list = repositories.getAllFavouritesByUser(user)
        mapped_favourites = []

        for favourite in favourite_list:
            
            nasa_card = '' # transformamos cada favorito en una NASACard, y lo almacenamos en nasa_card.
            nasa_card=mapper.fromRepositoryIntoNASACard(favourite)
            mapped_favourites.append(nasa_card)

        return mapped_favourites


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.

#nuevo usuario

def saveNewuser(request):
    usuario = request.POST.get('usuario', '')
    nombre = request.POST.get('nombre', '')
    apellido = request.POST.get('apellido', '')
    passw = request.POST.get('pass', '')
    email = request.POST.get('email', '')
    user=[]
    user.append(usuario)
    user.append(nombre)
    user.append(apellido)
    hash = django_pbkdf2_sha256.hash(passw)
    user.append(hash)
    user.append(email)

    # fav=mapper.fromTemplateIntoNASACard(request)
    # user = get_user(request)
    #  # transformamos un request del template en una NASACard.
    # fav.user = user # le seteamos el usuario correspondiente.

    return repositories.saveNewuser(user) # lo guardamos en la base.
