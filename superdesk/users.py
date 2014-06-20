"""Superdesk Users"""

import superdesk


class EmptyUsernameException(Exception):
    def __str__(self):
        return """Username is empty"""


class ConflictUsernameException(Exception):
    def __str__(self):
        return "Username '%s' exists already" % self.args[0]


def get_display_name(user):
    if user.get('first_name') or user.get('last_name'):
        display_name = '%s %s' % (user.get('first_name'), user.get('last_name'))
        return display_name.strip()
    else:
        return user.get('username')


def on_read_users(data, docs):
    """Set default fields for users"""
    for doc in docs:
        doc.setdefault('display_name', get_display_name(doc))
        if doc.get('password'):
            del doc['password']


class CreateUserCommand(superdesk.Command):
    """Create a user with given username and password.
    If user with given username exists, reset password.
    """

    option_list = (
        superdesk.Option('--username', '-u', dest='username'),
        superdesk.Option('--password', '-p', dest='password'),
    )

    def run(self, username, password):
        if username and password:
            userdata = {
                'username': username,
                'password': password,
            }

            user = superdesk.app.data.find_one('users', username=userdata.get('username'))
            if user:
                superdesk.app.data.update('users', user.get('_id'), userdata)
                return user
            else:
                superdesk.app.data.insert('users', [userdata])
                return userdata


superdesk.connect('read:users', on_read_users)
superdesk.connect('created:users', on_read_users)
superdesk.command('users:create', CreateUserCommand())

users_config = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },
    'schema': {
        'username': {
            'type': 'string',
            'unique': True,
            'required': True,
            'minlength': 1
        },
        'password': {
            'type': 'string',
            'minlength': 5
        },
        'first_name': {
            'type': 'string',
        },
        'last_name': {
            'type': 'string',
        },
        'display_name': {
            'type': 'string',
        },
        'email': {
            'unique': True,
            'type': 'email',
        },
        'phone': {
            'type': 'phone_number',
        },
        'user_info': {
            'type': 'dict'
        },
        'picture_url': {
            'type': 'string',
        },
        'role': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'user_roles',
                'field': '_id',
                'embeddable': True
            }
        },
        'workspace': {
            'type': 'dict'
        }
    },
    'extra_response_fields': [
        'display_name',
        'username',
        'email',
        'user_info',
        'picture_url',
    ],
    'datasource': {
        'projection': {
            'password': 0
        }
    },
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
}


def init_app(app):
    app.register_resource('users', users_config)
