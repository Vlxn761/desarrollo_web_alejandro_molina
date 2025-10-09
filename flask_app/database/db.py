from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref, joinedload
from datetime import datetime

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# --- Models ---

class AvisoAdopcion(Base):
    __tablename__ = 'aviso_adopcion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=True)
    celular = Column(String(15))
    tipo = Column(Enum('gato', 'perro'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum('a', 'm'), nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(Text)

    comuna = relationship("Comuna", back_populates="avisos_adopcion")
    contactos = relationship("ContactarPor", back_populates="aviso")
    fotos = relationship("Foto", back_populates="aviso")

class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship("Region", back_populates="comunas")
    avisos_adopcion = relationship("AvisoAdopcion", back_populates="comuna")

class ContactarPor(Base):
    __tablename__ = 'contactar_por'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), primary_key=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)

    aviso = relationship("AvisoAdopcion", back_populates="contactos")

class Foto(Base):
    __tablename__ = 'foto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), primary_key=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)

    aviso = relationship("AvisoAdopcion", back_populates="fotos")

class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    comunas = relationship("Comuna", back_populates="region")


# --- Database Functions ---
def get_avisos():
    session = SessionLocal()
    avisos = session.query(AvisoAdopcion).order_by(AvisoAdopcion.id.desc())
    session.close()
    return avisos

def get_aviso_by_id(id):
    session = SessionLocal()
    avisos = session.query(AvisoAdopcion).filter_by(id=id).first()
    session.close()
    return avisos

def get_avisos_recientes(max):
    session = SessionLocal()
    avisos = session.query(AvisoAdopcion).order_by(AvisoAdopcion.id.desc()).limit(max).all()
    session.close()
    return avisos


def get_paginated_avisos(offset):
    session = SessionLocal()
    avisos = session.query(AvisoAdopcion).options(
        joinedload(AvisoAdopcion.comuna),
        joinedload(AvisoAdopcion.fotos),
        joinedload(AvisoAdopcion.contactos)).order_by(AvisoAdopcion.id.desc())

    paginas = avisos.count()
    avisos = avisos.offset(offset).limit(5).all()
    session.close()
    return avisos, paginas

def get_foto_by_aviso(aviso_id, cantidad):
    session = SessionLocal()
    foto = session.query(Foto).filter_by(aviso_id=aviso_id).limit(cantidad).all()
    session.close()
    return foto

def get_fotos_by_aviso(aviso_id):
    session = SessionLocal()
    foto = session.query(Foto).filter_by(aviso_id=aviso_id).all()
    session.close()
    return foto

def get_comuna_by_id(id):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(id=id).first()
    session.close()
    return comuna

def get_comuna_by_name(name):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(nombre=name).first()
    session.close()
    return comuna

def get_region_by_id(id):
    session = SessionLocal()
    region = session.query(Region).filter_by(id=id).first()
    session.close()
    return region

def get_region_by_name(name):
    session = SessionLocal()
    region = session.query(Region).filter_by(nombre=name).first()
    session.close()
    return region

def get_contactos_by_aviso(aviso_id):
    session = SessionLocal()
    contacto = session.query(ContactarPor).filter_by(aviso_id=aviso_id).all()
    session.close()
    return contacto

def create_aviso(comuna, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha, descripcion):
    session = SessionLocal()
    comuna_id = get_comuna_by_name(comuna).id
    new_aviso = AvisoAdopcion(fecha_ingreso=datetime.now(),
                              comuna_id=comuna_id,
                              sector=sector,
                              nombre=nombre,
                              email=email,
                              celular=celular,
                              tipo=tipo,
                              cantidad=cantidad,
                              edad=edad,
                              unidad_medida=unidad_medida,
                              fecha_entrega=fecha,
                              descripcion=descripcion,
                              )
    session.add(new_aviso)
    session.commit()
    aviso_id = new_aviso.id
    session.close()
    return aviso_id

def create_contactarPor(aviso_id, nombre, identificador):
    session = SessionLocal()
    new_contacto = ContactarPor(aviso_id=aviso_id, nombre=nombre, identificador=identificador)
    session.add(new_contacto)
    session.commit()
    session.close()

def create_foto(aviso_id, filename):
    session = SessionLocal()
    new_foto = Foto(aviso_id=aviso_id, ruta_archivo=f"static/uploads/{filename}", nombre_archivo=filename)
    session.add(new_foto)
    session.commit()
    session.close()


def get_user_by_id(id):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(id=id).first()
    session.close()
    return user

def get_user_by_id(id):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(id=id).first()
    session.close()
    return user

def get_user_by_email(email):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(email=email).first()
    session.close()
    return user

def get_user_by_username(username):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(username=username).first()
    session.close()
    return user

def create_user(username, password, email):
    session = SessionLocal()
    new_user = Usuario(username=username, password=password, email=email)
    session.add(new_user)
    session.commit()
    session.close()

def get_confessions(page_size):
    session = SessionLocal()
    confesiones = session.query(Confesion).limit(page_size).all()
    session.close()
    return confesiones

def create_confession(conf_title, conf_text, conf_img, user_id):
    session = SessionLocal()
    new_confession = Confesion(conf_title=conf_title,conf_text=conf_text, conf_img=conf_img, user_id=user_id)
    session.add(new_confession)
    session.commit()
    session.close()

def change_profile_picture(username, new_img):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(username=username).first()
    if user:
        user.profile_image = new_img
        session.commit()
    session.close()

def get_profile_picture(username):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(username=username).first()
    if user:
        profile_image = user.profile_image
    else:
        profile_image = None
    session.close()
    return profile_image

def register_user(username, password, email):
    if get_user_by_email(email) is not None:
        return False, "El correo ya esta en uso."
    
    if get_user_by_username(username) is not None:
        return False, "El nombre de usuario esta en uso."
    
    create_user(username, password, email)
    return True, None

def login_user(username, password):
    a_user = get_user_by_username(username)
    if a_user is None:
        return False, "Usuario o contraseña incorrectos."
    
    if a_user.password != password:
        return False, "Usuario o contraseña incorrectos."
    
    return True, None
