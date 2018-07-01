import unittest

from app import db
from app.models import User
from tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            name="ken",
            username="testing"
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.u_id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            name="ken",
            username="testing"
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.u_id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 1)

if __name__ == '__main__':
    unittest.main()