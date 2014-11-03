from apps.auth import AuthResource
from .reset_password import ResetPasswordService, ResetPasswordResource, ActiveTokensResource
import superdesk
from .db import DbAuthService
from .commands import CreateUserCommand, HashUserPasswordsCommand  # noqa
from superdesk.services import BaseService
from flask import current_app as app
from superdesk.utils import get_hash


def update_password(updates, original):
    password = updates.get('password', None)
    if password and not password.startswith('$2a$'):
        updates['password'] = get_hash(password, app.config.get('BCRYPT_GENSALT_WORK_FACTOR', 12))


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

    app.on_update_users += update_password
