# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py
#import de la libreria passlib para el login encriptacion y desencriptacion
from passlib.hash import django_pbkdf2_sha256
#import de sqllite para BASE DE DATOS
import sqlite3
#libreria de django para autenticar usuarios
from django.contrib.auth.models import User
#libreria de django para autenticar usuarios
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = []
    images=services_nasa_image_gallery.getAllImages(input=None)

    favourite_list = []

    return images

# función principal de la galería.
def home(request):
    
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    images = []
    images=services_nasa_image_gallery.getAllImages(input=None)
    

    favourite_list = []
    favourite_list=services_nasa_image_gallery.getAllFavouritesByUser(request)
    #paginado

    paginadoimagenes = Paginator(images,5)

    # contact_list = Contact.objects.all()
    # paginator = Paginator(contact_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginadoimagenes.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj,'favourite_list': favourite_list})
    # return render(request, 'home.html', {'images': images,'favourite_list': favourite_list})


# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get('username', '')
    #revisa si es vacio para agregar por default "space"
    #  if search_msg == '' :
    #      search_msg == 'space'
        

    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    pass

#funcion de login view
def loginrequest(request):
    return render(request, 'registration/login.html')

#funcion de ingreso del usuario(login)

def ingresar(request):

    usuario = request.POST.get('username', '')
    password = request.POST.get('password', '')


    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT * FROM auth_user where username ='"'"+usuario+"'"'')
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        fila= row
    
    
    if django_pbkdf2_sha256.verify(password, fila[1]) == True:
        # user = User.objects.create_user("admin", "admin")

        user = authenticate(username="admin", password="admin")
        if user is not None:
                    login(request, user)
                    return render(request, 'home.html')
        else:
                   return render(request, 'home.html')
    
    else:
        return 'error'
#función de deslogeo

# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):

    favourite_list = []
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    services_nasa_image_gallery.saveFavourite(request)
    return render(request, 'home.html')
    pass


@login_required
def deleteFavourite(request):
    services_nasa_image_gallery.deleteFavourite(request)
    favourite_list = []
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})
    pass


@login_required
def exit(request):
    logout(request)
    return render(request, 'index.html')