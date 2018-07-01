from app import db
from app.models import User

def test_decode_auth_token():
    user = User(
        name="testing",
        username="testing",
        email="testing@testing",
        password="testing"
    )
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.u_id)
    print(isinstance(auth_token, bytes))
    print(User.decode_auth_token(auth_token) == 1)

