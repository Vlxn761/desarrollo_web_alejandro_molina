from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_cors import cross_origin
from utils.validations import validate_aviso, validate_comentario
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import uuid

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# --- Agregar aviso ---

@app.route("/agregar", methods=["GET", "POST"])
def agregar_aviso():
    if request.method == "POST":
        region = request.form.get("select-region")
        comuna = request.form.get("select-comuna")
        sector = request.form.get("sector")

        nombre = request.form.get("nombre")
        email = request.form.get("email")
        celular = request.form.get("tel")
        red = request.form.getlist("red-select")
        identificador = request.form.getlist("contacto")
  
        tipo = request.form.get("select-mascota")
        cantidad = request.form.get("cantidad")
        edad = request.form.get("edad")
        unidad_medida = request.form.get("select-unidad").lower()[0]
        fecha = request.form.get("fecha")
        fotos = request.files.getlist("foto")
        descripcion = request.form.get("descripcion")
        
        validate = validate_aviso(region, comuna, sector, nombre, email, tipo, cantidad, edad, unidad_medida, fecha, fotos)

        if validate:
            aviso_id = db.create_aviso(comuna,
                                        sector,
                                        nombre,
                                        email,
                                        celular,
                                        tipo,
                                        cantidad,
                                        edad,
                                        unidad_medida,
                                        fecha,
                                        descripcion)

            for i in range(0, len(red)):
                db.create_contactarPor(aviso_id, red[i], identificador[i])

            for foto in fotos:
                _filename = hashlib.sha256(
                    secure_filename(foto.filename).encode("utf-8")
                ).hexdigest()
                _extension = filetype.guess(foto).extension
                img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"

                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
                db.create_foto(aviso_id, img_filename)

            return redirect(url_for("index"))

    elif request.method == "GET":
        return render_template("agregar_aviso/formulario.html")
    
# --- Listado de adopciones ---

@app.route("/adopciones", methods=["GET"])
def listado():
    if request.method == "GET":
        aviso = db.get_avisos()
        pagina = request.args.get("page", 1, type=int)

        avisos, total = db.get_paginated_avisos(5*(pagina-1))

        data = []

        for aviso in avisos:
            comuna = db.get_comuna_by_id(aviso.comuna_id)

            tipo = aviso.tipo + 's' if aviso.cantidad > 1 else aviso.tipo

            unidad_medida = "año"
            if aviso.edad > 1:
                unidad_medida += "s"
            if aviso.unidad_medida == 'm':
                unidad_medida = "mes"
                if aviso.edad > 1:
                    unidad_medida += "es"

            fotos = db.get_fotos_by_aviso(aviso.id)

            data.append({
                "id": aviso.id,
                "fecha_publicacion": aviso.fecha_entrega,
                "fecha_entrega": aviso.fecha_ingreso,
                "comuna": comuna.nombre,
                "sector": aviso.sector,
                "detalles": f"{aviso.cantidad} {tipo} {aviso.edad} {unidad_medida}",
                "nombre": aviso.nombre,
                "total_fotos": len(fotos)
            })

        return render_template("listado/listado.html", data = data, page=pagina, total = total)

# --- Aviso detallado ---

@app.route("/info/<int:id>", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def informacion_aviso(id):
    aviso = db.get_aviso_by_id(id)

    comuna = db.get_comuna_by_id(aviso.comuna_id)
    region = db.get_region_by_id(comuna.region_id)

    contacto = db.get_contactos_by_aviso(aviso.id)

    fotos = db.get_foto_by_aviso(aviso.id, 5)

    unidad_medida = "Meses"
    if aviso.unidad_medida == "a":
        unidad_medida = "Años"    

    tipo = "Gato"
    if aviso.tipo == "perro":
        tipo = "Perro"    

    data = {
        "id": id,
        "region": region.nombre,
        "comuna": comuna.nombre,
        "sector": aviso.sector,
        "nombre": aviso.nombre,
        "email": aviso.email,
        "celular": aviso.celular,
        "contacto": contacto,
        "tipo": tipo,
        "cantidad": aviso.cantidad,
        "edad": aviso.edad,
        "unidad": unidad_medida,
        "foto": fotos
    }

    comentarios = db.get_comentarios_by_aviso(id)
    data_comentarios = []

    for comentario in comentarios:
        data_comentarios.append({
            "nombre": comentario.nombre,
            "fecha": comentario.fecha,
            "texto": comentario.texto
        })

    if data is None:
        return render_template("informacion_aviso/informacion_aviso.html", error="Aviso no encontrado")


    return render_template("informacion_aviso/informacion_aviso.html", data=data, comments=data_comentarios)    

@app.route("/comentarios/<int:id>", methods=["GET", "POST"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def comentarios_aviso(id):
    if request.method == "POST":
        form = request.get_json()
        nombre = form["nombre"]
        texto = form["texto"]
        
        validate = validate_comentario(nombre, texto)

        if validate:
            db.create_comentario(id, nombre, texto)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "error", "data": "Comentario invalido"}), 400
        
    elif request.method == "GET":
        comentarios = db.get_comentarios_by_aviso(id)

        data = []

        for comentario in comentarios:
            data.append({
                "nombre": comentario.nombre,
                "texto": comentario.texto,
                "fecha": comentario.fecha.strftime("%Y-%m-%d %H:%M")
            })
    
        return jsonify(data)

# --- Estadísticas ---

@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    return render_template("estadisticas/estadisticas.html")

@app.route("/estadisticas-dia", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def obtener_datos_dia():
    data = []
    avisos = db.get_avisos_diarios()
    for fecha in avisos:
        data.append({
            "fecha": fecha.strftime("%Y-%m-%d"),
            "cantidad": avisos[fecha]
        })
    data.sort(key=lambda x: x["fecha"])

    return jsonify(data)

@app.route("/estadisticas-tipo", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def obtener_datos_tipo():
    data = []
    avisos = db.get_avisos_tipo()
    for tipo in avisos:
        data.append({
            "tipo": tipo,
            "cantidad": avisos[tipo]
        })

    return jsonify(data)

@app.route("/estadisticas-mes", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def obtener_datos_mes():
    dataPerros = list(range(12))
    dataGatos = list(range(12))
    avisos = db.get_avisos_mes()
    for i in range(12):
        dataPerros[i] = avisos[i]["Perros"]
        dataGatos[i] = avisos[i]["Gatos"]

    return jsonify({
        "perros": dataPerros, 
        "gatos": dataGatos
        })

# --- Index ---

@app.route("/", methods=["GET"])
def index():
    data = []
    for aviso in db.get_avisos_recientes(5):
        
        img = db.get_foto_by_aviso(aviso.id, 1)
        
        if img:
            img = img[0].ruta_archivo
        else:
            img = "static/svg/3gatos.jpg"

        comuna = db.get_comuna_by_id(aviso.comuna_id)

        tipo = aviso.tipo + 's' if aviso.cantidad > 1 else aviso.tipo

        unidad_medida = "año"
        if aviso.edad > 1:
            unidad_medida += "s"
        if aviso.unidad_medida == 'm':
            unidad_medida = "mes"
            if aviso.edad > 1:
                unidad_medida += "es"

        data.append({
            "fecha": aviso.fecha_entrega,
            "comuna": comuna.nombre,
            "sector": aviso.sector,
            "detalles": f"{aviso.cantidad} {tipo} {aviso.edad} {unidad_medida}",
            "ruta_imagen": img
        })
        
    return render_template("portada/portada.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
