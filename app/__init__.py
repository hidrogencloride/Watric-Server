import os
from flask import Flask, render_template, send_file, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, static_url_path='/app/static/images')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from models import Result ; Example code for future reference

from models import User

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/main')
def home():
    return render_template("landing-page.html")


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
    remember = BooleanField('remember me')


@app.route('/login')
def login():
    form = LoginForm()
    error = None
    global current_user
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user:
            hashed_password = generate_password_hash(user.password, method='sha256')
            if check_password_hash(hashed_password, form.password.data):
                app.logger.debug('Logged in user %s', user.username)
                login_user(user, remember=form.remember.data)
                current_user = user
                return redirect(url_for('/main'))
        error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@app.route('/images/<string:image>')
def return_image(image):
    filename = os.path.join(app.instance_path,'static', 'images', image).replace("instance", "app")
    return send_file(filename, mimetype="image/gif")

@app.route("/static/<string:js>")
def return_js(js):
    filename = os.path.join(app.instance_path,"static", js).replace("instance", "app")
    return send_file(filename, mimetype="application/javascript")
