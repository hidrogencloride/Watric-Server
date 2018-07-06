import os
from flask import Flask, render_template, send_file, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://urbqqmuwbhzhqx:2845b320cf6c248880c4772ec1c63195f2e26dca68cad6f74efb4c2c590fee96@ec2-50-16-241-91.compute-1.amazonaws.com:5432/d1ef3bj6g3k7fg"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BIND'] = True

db = SQLAlchemy(app)

# Imports need to be done after db is initialized
from app.models import *
from Blueprints.AdminPage import admin_page

db.create_all()

app.register_blueprint(admin_page)

# from models import Result ; Example code for future reference

@app.route('/main')
def home():
    return render_template("landing-page.html")


@app.route('/products')
def load_products():
    products = Products.query.filter(Products.accessory==False).all()
    mapped_result = []
    for p in products:
        mapped_result.append({'p_id': p.p_id, 'p_name': p.p_name, 'price': p.price, 'accessory': p.accessory})
    return jsonify(mapped_result)


@app.route('/products/accessories')
def load_accessories():
    products = Products.query.filter(Products.accessory==True).all()
    mapped_result = []
    for p in products:
        mapped_result.append({'p_id': p.p_id, 'p_name': p.p_name, 'price': p.price, 'accessory': p.accessory})
    return jsonify(mapped_result)


@app.route('/images/<string:image>')
def return_image(image):
    filename = os.path.join(app.instance_path,'static', 'images', image).replace("instance", "app")
    return send_file(filename, mimetype="image/gif")

@app.route("/static/<string:js>")
def return_js(js):
    filename = os.path.join(app.instance_path,"static", js).replace("instance", "app")
    return send_file(filename, mimetype="application/javascript")
