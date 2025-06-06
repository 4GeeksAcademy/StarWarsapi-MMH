"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planeta, Personaje,Favorito
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def handle_people():

    people = Personaje.query.all()
    people_serialize = [person.serialize() for person in people]
    return jsonify(people_serialize), 200


@app.route('/people/<int:id>', methods=['GET'])
def get_one_person(id):
    
    gente = Personaje.query.get(id)
    if gente is None:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(gente.serialize()), 200

@app.route('/planet', methods=['GET'])
def handle_planets():

    planets = Planeta.query.all()
    planets_serialize = [planeta.serialize() for planeta in planets]
    return jsonify(planets_serialize), 200

#Ruta planeta por id
@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):

    planeta = Planeta.query.get(id)
    if planeta is None:
        return jsonify({"error": "planeta no encontrado"}), 404
    return jsonify(planeta.serialize()), 200

#Ruta que muestre todos los usuarios

@app.route('/user', methods=['GET'])
def handle_users():

    usuarios = User.query.all()
    usuarios_serialize = [usuario.serialize() for usuario in usuarios]
    return jsonify(usuarios_serialize), 200

#Ruta que muestro un usuario por id

@app.route('/user/<int:id>', methods=['GET'])
def get_one_usuario(id):

    users = User.query.get(id)
    if users is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(users.serialize()), 200

# Ruta para agregar favorito planetas
@app.route('/favoritos/planeta/<int:id>', methods=['POST'])
def add_datos(id):

    
    add_favorito = Favorito(
        user_id=1,
        planeta_id =id
    )
    db.session.add(add_favorito)
    db.session.commit()
    return jsonify({"msg":"Planeta favorito agregado"}), 201

    

    





# Ruta para agregar favorito people





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
