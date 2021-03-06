import jwt

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions

from jwt import DecodeError


User = get_user_model()

from rest_framework.authentication import BaseAuthentication, get_authorization_header


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None
        else:
            token = auth[1]
            try:
                key = jwt.decode(token, settings.SECRET_KEY)
            except DecodeError:
                msg = 'Signature verification failed. Invalid token.'
                raise exceptions.ValidationError(msg)
            return self.authenticate_credentials(key.get('email'))

    def authenticate_credentials(self, email):
        user = User.objects.get(email=email)
        return user, None


def token_encode(data):
    return {
        'token': jwt.encode({"email": data.get('email')}, settings.SECRET_KEY).decode(),
    }


def token_decode(token):
    return jwt.decode(token, settings.SECRET_KEY)
