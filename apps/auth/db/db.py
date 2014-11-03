import bcrypt
from apps.auth.errors import NotFoundAuthError, raiseCredentialsAuthError
from apps.auth.service import AuthService
from flask import current_app as app


class DbAuthService(AuthService):

    def authenticate(self, credentials):
        user = app.data.find_one('auth_users', req=None, username=credentials.get('username'))
        if not user:
            raise NotFoundAuthError()

        password = credentials.get('password').encode('UTF-8')
        hashed = user.get('password').encode('UTF-8')

        if not (password and hashed):
            raiseCredentialsAuthError(credentials)

        try:
            rehashed = bcrypt.hashpw(password, hashed)
            if hashed != rehashed:
                raiseCredentialsAuthError(credentials)
        except ValueError:
            raiseCredentialsAuthError(credentials)

        return user
