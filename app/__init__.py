import os
from flask import Flask, render_template, send_file, url_for, request, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
# from flask_cors import CORS

app = Flask(__name__, static_url_path='/app/static/images')
# cors = CORS(app, resources={r"/auth/*": {"origins":"*"}})
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# from models import Result ; Example code for future reference

from app.models import *
from Blueprints.AdminBlueprint import admin_page

db.create_all()

app.register_blueprint(admin_page)

# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route('/main')
def home():
    return render_template("landing-page.html")

### Syncronous login attempt ##
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
#
#
# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
#     password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
#     remember = BooleanField('remember me')
#
#
# @app.route('/login')
# def login():
#     form = LoginForm()
#     error = None
#     global current_user
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data.lower()).first()
#         if user:
#             hashed_password = generate_password_hash(user.password, method='sha256')
#             if check_password_hash(hashed_password, form.password.data):
#                 app.logger.debug('Logged in user %s', user.username)
#                 login_user(user, remember=form.remember.data)
#                 current_user = user
#                 return redirect(url_for('/main'))
#         error = 'Invalid username or password.'
#     return render_template('login.html', form=form, error=error)

### end of synchronous login attempt ###


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


### start of auth restful api for stateless authentication using jwt ###
@app.route("/auth/register", methods=["POST"])
def register():
    post_data = request.get_json()
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        try:
            user = User(
                name=post_data.get("name"),
                username=post_data.get("username"),
                password=post_data.get("password"),
                email=post_data.get("email")
            )
            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token(user.u_id)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 201

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202

@app.route("/auth/login", methods=["POST"])
def restful_login():
    post_data = request.get_json()
    try:
        # fetch the user data
        user = User.query.filter_by(
            email=post_data.get('email')
        ).first()

        if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
        ):
            auth_token = user.encode_auth_token(user.u_id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 404
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500


### Gets the info of the current logged in user using the id encrypted in the jwt token
@app.route("/auth/status")
def getStatus():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(u_id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.u_id,
                    'email': user.email,
                    'name': user.name,
                    'purchases': user.purchases
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401

@app.route('/auth/logout', methods=['POST'])
def restful_logout():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403
