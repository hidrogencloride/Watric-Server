import os
from flask import Flask, render_template, send_file, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://urbqqmuwbhzhqx:2845b320cf6c248880c4772ec1c63195f2e26dca68cad6f74efb4c2c590fee96@ec2-50-16-241-91.compute-1.amazonaws.com:5432/d1ef3bj6g3k7fg"
# engine = create_engine("postgres://urbqqmuwbhzhqx:2845b320cf6c248880c4772ec1c63195f2e26dca68cad6f74efb4c2c590fee96@ec2-50-16-241-91.compute-1.amazonaws.com:5432/d1ef3bj6g3k7fg")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BIND'] = True

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

# Session = sessionmaker(bind=engine)
# Session.configure(bind=engine)
# session = Session()

# from models import Result ; Example code for future reference

from app.models import User, Products

# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route('/main')
def home():
    return render_template("landing-page.html")


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
    remember = BooleanField('remember me')


class RegisterForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[InputRequired(), Length(min=6, max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=50), EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        print('not validated: ')
        print(form.data)
        if form.validate():
            print('validated: ')
            print(form.data)
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data

            # Add new user to the data base
            # new_user = User(name=name, email=email, username=username, password=password)
            # session.add(new_user)
            # session.commit()

            return redirect(url_for('/main'))

    return render_template('register.html', form=form)


@app.route('/products')
def load_products():
    return db.session.query(Products).filter(not Products.accessory).all()


@app.route('/images/<string:image>')
def return_image(image):
    filename = os.path.join(app.instance_path,'static', 'images', image).replace("instance", "app")
    return send_file(filename, mimetype="image/gif")

@app.route("/static/<string:js>")
def return_js(js):
    filename = os.path.join(app.instance_path,"static", js).replace("instance", "app")
    return send_file(filename, mimetype="application/javascript")

if __name__ == '__main__':
    app.run()