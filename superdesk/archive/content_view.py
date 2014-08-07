
import flask
import logging
import superdesk

from eve.utils import ParsedRequest
from superdesk.base_model import BaseModel
from flask import json

logger = logging.getLogger(__name__)


class ContentViewModel(BaseModel):
    endpoint_name = 'content_view'
    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'minlength': 1
        },
        'description': {
            'type': 'string',
        },
        'desk': {
            'type': 'objectid'
        },
        'user': {
            'type': 'objectid'
        },
        'filter': {
            'type': 'dict'
        }
    }

    def check_filter(self, filter, location='archive'):
        # TOOD: change this after refactoring Eve to avoid direct access to request
        # object on datalayer
        parsed_request = ParsedRequest()
        parsed_request.args = {'source': json.dumps({'query': {'filtered': {'filter': filter}}})}
        payload = None
        try:
            superdesk.apps[location].get(req=parsed_request, lookup={})
        except Exception as e:
            logger.exception(e)
            payload = 'Fail to validate the filter against %s.' % location
        if payload:
            raise superdesk.SuperdeskError(payload=payload)

    def process_and_validate(self, doc):
        if 'filter' in doc and doc['filter']:
            self.check_filter(doc['filter'])

    def on_create(self, docs):
        for doc in docs:
            doc.setdefault('user', flask.g.user['_id'])
            self.process_and_validate(doc)

    def on_update(self, updates, original):
        self.process_and_validate(updates)
