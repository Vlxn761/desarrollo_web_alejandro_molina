import re
import filetype
import database.db as db
from datetime import datetime, timedelta

def validate_region(region):
    region = db.get_region_by_name(region)
    if region:
        return True
    return False

def validate_comuna(comuna):
    comuna = db.get_comuna_by_name(comuna)
    if comuna:
        return True
    return False

def validate_lugar(comuna_nombre, region_nombre): 
    if validate_comuna(comuna_nombre) and validate_region(region_nombre):
        comuna = db.get_comuna_by_name(comuna_nombre)
        region = db.get_region_by_name(region_nombre)
        region2 = db.get_region_by_id(comuna.region_id)
        if region2:
            return region2.id == region.id
    return False

def validate_sector(sector):
    if len(sector) >= 100:
        return False
    return True

def validate_nombre(nombre):
    if nombre:
        if len(nombre) >= 3 and len(nombre) < 200:
            return True
    return False

def validate_email(email):
    if email:
        r = r'^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
        return len(email) <= 100 and bool(re.match(r, email))
    return False

def validate_celular(celular):
    if celular:
        r = r'/^\+\d{3}\.\d{8}$/'
        return bool(re.match(r, celular))
    return False

def validate_red(red):
    if red:
        return red in ["Whatsapp", "Telegram", "Instagram", "X", "TikTok", "Otra"]
    return False

def validate_redes(redes):
    if len(red) > 5:
        return False
    for red in redes:
        if not validate_red(red):
            return False
    return True

def validate_identificador(identificador):
    return len(identificador) >= 4 and len(identificador) <= 50

def validate_identificadores(identificadores):
    for identificador in identificadores:
        if not validate_identificador(identificador):
            return False
    return True

def validate_tipo(tipo): 
    if tipo:
        return tipo in ["Perro", "Gato"]
    return False

def validate_cantidad(cantidad):
    if cantidad:
        return cantidad.isdigit() and int(cantidad) > 0
    return False

def validate_edad(edad):
    if edad:
        return edad.isdigit() and int(edad) > 0            
    return False

def validate_unidad_medida(unidad):
    if unidad:
        return unidad in ["m", "a"]
    return False

def validate_fecha(fecha):
    if fecha:
        pattern = re.compile(
            r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T([01]\d|2[0-3]):[0-5]\d$'
        )
        if bool(pattern.match(fecha)):
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%dT%H:%M")
            fecha_default = datetime.now() + timedelta(hours=2, minutes=55)
            return fecha_dt >= fecha_default
    return False

def validate_foto(img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if img is None:
        return False

    # check if the browser submitted an empty file
    if img.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validate_fotos(fotos):
    if len(fotos) < 1 or len(fotos) > 5:
        return False
    for foto in fotos:
        if not validate_foto(foto):
            return False
    return True


def validate_aviso(region, comuna, sector, nombre, email, tipo, cantidad, edad, unidad, fecha, fotos):
    validate = True

    if not validate_region(region):
        validate = False

    if not validate_comuna(comuna):
        validate = False

    if not validate_lugar(comuna, region):
        validate = False

    if not validate_sector(sector):
        validate = False

    if not validate_nombre(nombre):
        validate = False

    if not validate_email(email):
        validate = False

    if not validate_tipo(tipo):
        validate = False

    if not validate_cantidad(cantidad):
        validate = False

    if not validate_edad(edad):
        validate = False

    if not validate_unidad_medida(unidad):
        validate = False

    if not validate_fecha(fecha):
        validate = False

    if not validate_fotos(fotos):
        validate = False

    return validate