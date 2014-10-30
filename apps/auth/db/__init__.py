from apps.auth import AuthResource
from .reset_password import ResetPasswordService, ResetPasswordResource, ActiveTokensResource
import superdesk
from .db import DbAuthService
from .commands import CreateUserCommand, HashUserPasswordsCommand  # noqa
from superdesk.services import BaseService
from flask import current_app as app


def hash_password(users):
    for user in users:
        password = user.get('password', None)
        if password and not password.startswith('$2a$'):
            user['password'] = get_hash(password, app.config.get('BCRYPT_GENSALT_WORK_FACTOR', 12))


def init_app(app):
    endpoint_name = 'auth'
    service = DbAuthService(endpoint_name, backend=superdesk.get_backend())
    AuthResource(endpoint_name, app=app, service=service)

    endpoint_name = 'reset_user_password'
    service = ResetPasswordService(endpoint_name, backend=superdesk.get_backend())
    ResetPasswordResource(endpoint_name, app=app, service=service)

    endpoint_name = 'active_tokens'
    service = BaseService(endpoint_name, backend=superdesk.get_backend())
    ActiveTokensResource(endpoint_name, app=app, service=service)

    app.on_update_users += hash_password
