# capa DAO de acceso/persistencia de datos.

from nasa_image_gallery.models import Favourite
from datetime import datetime
import sqlite3
from django.contrib.auth.models import User

def saveFavourite(image):
    try:
        fav = Favourite.objects.create(title=image.title, description=image.description, image_url=image.image_url, date=image.date, user=image.user)
        return fav
    except Exception as e:
        print(f"Error al guardar el favorito: {e}")
        return None

def getAllFavouritesByUser(user):
    favouriteList = Favourite.objects.filter(user=user).values('id', 'title', 'description', 'image_url', 'date')
    return list(favouriteList)

def deleteFavourite(id):
    try:
        favourite = Favourite.objects.get(id=id)
        favourite.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {id} no existe.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False
    
def saveNewuser(user):
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        sql = 'insert into auth_user (password,is_superuser,username,last_name,email,is_staff,is_active,date_joined,first_name) values ('"'"+user[3]+"',1,'"+user[2]+"','"+user[1]+"','"+user[4]+"',1,1,'"+str(datetime.now())+"','"+user[0]+"')"
        cur.execute(sql)
        conn.commit()
        conn.close()
        user = User.objects.create_user(username=user[2],
                                        email=user[4],
                                        password=user[3])
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error al guardar el favorito: {e}")
        return None
    
