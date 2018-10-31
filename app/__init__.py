import os, base64
from flask import Flask, render_template, send_file, url_for, request, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/auth/*": {"origins":"*"}})
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from app.models import *
from Blueprints.AdminBlueprint import admin_page
from Blueprints.AuthBlueprint import auth_api

db.create_all()

app.register_blueprint(admin_page)
app.register_blueprint(auth_api)

def add_product():
    images = [
        {
            "p_name": "Black_Hoodie_1",
            "price": 50,
        },
        {
            "p_name": "Black_Hoodie_2",
            "price":50
        },
        {
            "p_name:Black_Hoodie_3",
            "price"
        }
    ]


@app.route('/')
def home():
    return render_template("landing-page.html")

@app.route('/croqui')
def croqui():
    return render_template("croqui.html")

@app.route('/water')
def water():
    return render_template("water.html")

@app.route('/naturalWind')
def naturalWind():
    return render_template("naturalWind.html")

@app.route('/nonNaturalWind')
def nonNaturalWind():
    return render_template("nonNaturalWind.html")

@app.route('/illumination')
def illumination():
    return render_template("illumination.html")

@app.route('/supportUs')
def videoTest():
    return render_template("supportUs.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/sitemap')
def sitemap():
    return render_template("sitemap.xml")

### Resources routes ###
@app.route('/images/<string:image>')
def return_image(image):
    filename = os.path.join(app.instance_path,'static', 'images', image).replace("instance", "app")
    return send_file(filename, mimetype="image/gif")

@app.route("/static/<string:js>")
def return_js(js):
    filename = os.path.join(app.instance_path,"static", js).replace("instance", "app")
    return send_file(filename, mimetype="application/javascript")


@app.route("/get_misc")
def get_misc():
    folder_path = os.path.join(app.instance_path, "private_images", "asseccories" ).replace("instance", "app")
    directory = os.fsencode(folder_path)
    r_objects = []
    for file in os.listdir(directory):
        print(file)
        print("\n")
        filename = os.fsdecode(file)
        response_object = {}
        with open(os.path.join(folder_path, filename), "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            response_object["image"] = encoded
            if "black-hoodie" in filename or "white-hoodie" in filename:
                response_object["price"] = 50
                response_object["name"] = filename.replace("_", " ").rstrip(".jpeg")
            elif "black-shirt" in filename or "white-shirt":
                response_object["price"] = 15
                response_object["name"] = filename.replace("_", " ").rstrip(".jpeg")
            else:
                response_object["price"] = 5
                response_object["name"] = filename.rstrip(".jpeg")
        r_objects.append(response_object)
    print(r_objects)
    return make_response(jsonify(r_objects)), 200




### end of resources routes ###




