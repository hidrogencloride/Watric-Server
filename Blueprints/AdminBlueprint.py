from flask import Blueprint, render_template, redirect, url_for, jsonify
from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo
from app.models import *


admin_page = Blueprint('admin_page', __name__)

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


@admin_page.route('/adminlogin')
def login():
    form = LoginForm()
    error = None
    global current_user
    if form.validate():
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


@admin_page.route('/create_admin')
def create_admin():
    return 'Nothing'

# No se necesita

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm(request.form)
#     if request.method == 'POST':
#         print('not validated: ')
#         print(form.data)
#         if form.validate():
#             print('validated: ')
#             print(form.data)
#             name = form.name.data
#             email = form.email.data
#             username = form.username.data
#             password = form.password.data
#
#             # Add new user to the data base
#             # new_user = User(name=name, email=email, username=username, password=password)
#             # session.add(new_user)
#             # session.commit()
#
#             return redirect(url_for('/main'))
#
#     return render_template('register.html', form=form)


@admin_page.route('/purchases')
def load_purchases():
    purchases = Purchases.query.all()
    mapped_result = []
    for p in purchases:
        mapped_result.append({'pu_id': p.pu_id, 'u_id': p.u_id, 'p_id': p.p_id, 'date': p.date})
    return jsonify(mapped_result)

@admin_page.route('/products')
def load_products():
    products = Products.query.all()
    mapped_result = []
    for p in products:
        mapped_result.append([p.p_id, p.p_name, p.price, p.accessory])
    return jsonify(Products=mapped_result)

@admin_page.route('/users')
def load_users():
    users = Users.query.all()
    mapped_result = []
    for u in users:
        mapped_result.append({'u_id': u.u_id, 'name': u.name, 'username': u.username, email: 'u.email'})
    return jsonify(Users=mapped_result)
