from flask import Blueprint, render_template, redirect, url_for, jsonify, make_response, request
from app.models import *
from app import db, bcrypt


auth_api = Blueprint('auth', __name__)


def get_auth_token():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    return auth_token


@auth_api.route("/auth/register", methods=["POST"])
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


@auth_api.route("/auth/login", methods=["POST"])
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
@auth_api.route("/auth/status")
def getStatus():
    auth_token = get_auth_token()
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(u_id=resp).first()
            responseObject = {
                'status': 'success',
                'data': user.to_dict()
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


@auth_api.route('/auth/logout', methods=['POST'])
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


@auth_api.route('/auth/add-address', methods=['POST'])
def add_address():
    auth_token = get_auth_token()
    post_data = request.get_json()
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            new_address = ShippingInfo(
                u_id=resp,
                address=post_data["address"],
                phone=post_data["phone"],
                state=post_data["state"],
                country=post_data["country"],
                postal_code=post_data["postal_code"],
                city=post_data["city"],
            )
            try:
                ship_info = ShippingInfo.query.filter_by(u_id=resp, address=post_data["address"],
                                                         state=post_data["state"], country=post_data["country"]).first()
                if ship_info:
                    raise Exception("User already has the address registered")
                else:
                    db.session.add(new_address)
                    db.session.commit()
                    newUser = User.query.filter_by(u_id=resp).first()
                    responseObject = {
                        'status': 'success',
                        'message': 'Shipping Address saved successfully',
                        'data':newUser.to_dict()
                    }
                    return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': str(e)
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status' : 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403


@auth_api.route('/auth/delete-address', methods=["POST"])
def delete_address():
    auth_token = get_auth_token()
    print(auth_token)
    post_data = request.get_json()
    print(post_data)
    if auth_token:
        print("inside first if")
        u_id = User.decode_auth_token(auth_token)
        if not isinstance(u_id, str):
            try:
                to_delete = ShippingInfo.query.filter_by(id=post_data["id"]).first()
                db.session.delete(to_delete)
                db.session.commit()
                new_user = User.query.filter_by(u_id=u_id).first()
                responseObject = {
                    'data': new_user.to_dict(),
                    'status':'success',
                    'message': 'Shipping Info was removed successfully'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': str(e)
                }
                return make_response(jsonify(responseObject)), 500
        else:
            responseObject = {
                'status': 'fail',
                'message': u_id
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide Valid Auth Token'
        }
        return make_response(jsonify(responseObject)), 403