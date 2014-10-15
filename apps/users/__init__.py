from .users import RolesResource, UsersResource
from .services import ADUsersService, DBUsersService
import superdesk
from superdesk.services import BaseService


def init_app(app):

    is_ldap = bool(app.config.get('LDAP_SERVER', False))

    endpoint_name = 'users'
    if is_ldap:
        service = ADUsersService(endpoint_name, backend=superdesk.get_backend())
    else:
        service = DBUsersService(endpoint_name, backend=superdesk.get_backend())

    UsersResource.readonly = is_ldap
    UsersResource(endpoint_name, app=app, service=service)

    endpoint_name = 'roles'
    service = BaseService(endpoint_name, backend=superdesk.get_backend())
    RolesResource(endpoint_name, app=app, service=service)
