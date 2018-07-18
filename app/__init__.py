import os
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


@app.route('/')
def home():
    return render_template("landing-page.html")

### Resources routes ###
@app.route('/images/<string:image>')
def return_image(image):
    filename = os.path.join(app.instance_path,'static', 'images', image).replace("instance", "app")
    return send_file(filename, mimetype="image/gif")

@app.route("/static/<string:js>")
def return_js(js):
    filename = os.path.join(app.instance_path,"static", js).replace("instance", "app")
    return send_file(filename, mimetype="application/javascript")
### end of resources routes ###



