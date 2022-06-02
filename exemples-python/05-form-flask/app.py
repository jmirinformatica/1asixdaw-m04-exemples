# pip3 install Flask
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import logging
import tempfile
import os

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return render_template("formularis.html")

@app.route('/exemple-de-get') # per defecte respon al mètode GET
def exemple_de_get():
    app.logger.info("Enviat formulari mitjançant GET")

    # diccionari de dades, on les keys són el valor de l'atribut "name"
    dades = request.args

    nom = dades.get("nom", None) #el segon paràmetre és el valor per defecte
    edat = dades.get("edat-en-anys", None)
    colors = dades.getlist("color-preferit") #llista de valors

    return render_template("dades-get.html", nom=nom, edat=edat, colors=colors)

@app.route('/exemple-de-post', methods=['POST']) # captura peticions POST
def exemple_de_post():
    app.logger.info("Enviat formulari mitjançant POST")

    # diccionari de dades, on les keys són el valor de l'atribut "name"
    dades = request.form

    ciutat = dades.get("ciutat", None)
    multiples_visites = dades.get("multiples-visites", "no") #que no envii res significa que ha dit que no
    tornaria = dades.get("tornaria", "no")
    comentaris = dades.get("comentaris", "Cap comentari")

    return render_template("dades-post.html", ciutat=ciutat, multiples_visites=multiples_visites, tornaria=tornaria, comentaris=comentaris)

@app.route('/exemple-de-post-amb-fitxers', methods=['POST']) # captura peticions POST
def exemple_de_post_amb_fitxers():
    app.logger.info("Enviat formulari mitjançant POST amb fitxers adjunts")

    fitxer = request.files.get("fitxer", None)

    # si el nom del fitxer és buït, significa que no s'ha pujat cap fitxer
    if fitxer is None or fitxer.filename == "":
        app.logger.warn("No s'ha pujat cap fitxer")

        ruta_fitxer = None
        ruta_imatge = "/static/img/error.png"
    else:
        # ens assegurem que el nom del fitxer és "correcte"
        nom_fitxer = secure_filename(fitxer.filename)

        # ruta absoluta de partida on es guardaran els fitxers pujats

        # vull guardar el fitxer a una subcarpeta dins de "/static/uploads"
        temp_dir = tempfile.mkdtemp(dir=app.root_path + "/static/uploads")

        # salvo el fitxer a la carpeta temporal que he creat
        ruta_absoluta_fitxer = temp_dir + "/" + nom_fitxer
        fitxer.save(ruta_absoluta_fitxer)

        app.logger.info(f"Pujat el fitxer {ruta_absoluta_fitxer}")

        # calculo la ruta relativa per passar-la al html
        ruta_fitxer = os.path.relpath(ruta_absoluta_fitxer, app.root_path)

        ruta_imatge = "/static/img/unknown.png"
        if is_img_file(fitxer.filename):
            ruta_imatge = ruta_fitxer

    return render_template("dades-post-fitxers.html", ruta_fitxer = ruta_fitxer, ruta_imatge = ruta_imatge)

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def is_img_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Necessari per iniciar un servidor de proves
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
