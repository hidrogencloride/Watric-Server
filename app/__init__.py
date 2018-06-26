import os
from flask import Flask, render_template, send_file, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='/app/static/images')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from models import Result ; Example code for future reference


@app.route('/')
def home():
    return render_template("landing-page.html")


@app.route('/images/<string:image>')
def return_image(image):
    filename = os.path.join(app.instance_path, 'static', 'images', image)
    return send_file(filename, mimetype="image/gif")

@app.route("/static/<string:js>")
def return_js(js):
    filename = os.path.join(app.instance_path, 'static', js)
    return send_file(filename, mimetype="image/gif")
