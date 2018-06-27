from app import db
from sqlalchemy.dialects.postgresql import JSON


# Example Code for future reference
# class Result(db.Model):
#     __tablename__ = 'results'
#
#     id = db.Column(db.Integer, primary_key=True)
#     url = db.Column(db.String())
#     result_all = db.Column(JSON)
#     result_no_stop_words = db.Column(JSON)
#
#     def __init__(self, url, result_all, result_no_stop_words):
#         self.url = url
#         self.result_all = result_all
#         self.result_no_stop_words = result_no_stop_words
#
#     def __repr__(self):
#         return '<id {}>'.format(self.id)

class User(db.Model):

    __tablename__ = "User"

    u_id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    purchases = db.relationship("Purchases", backref="User", lazy=False)

class Products(db.Model):

    __tablename__ = "Products"

    p_id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    accessory = db.Column(db.Boolean, nullable=False)


class Purchases(db.Model):

    __tablename__ = "Purchases"

    pu_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("User.u_id"), nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey("Products.p_id"), nullable=False )


