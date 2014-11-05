from ..models.item import ItemModel
from .item_lock import can_lock
from superdesk.utc import get_expiry_date
from superdesk.notification import push_notification
from apps.common.components.base_component import BaseComponent
from apps.common.models.utils import get_model
from superdesk import app, get_resource_service, SuperdeskError


IS_SPIKED = 'is_spiked'
EXPIRY = 'expiry'


class ItemSpike(BaseComponent):
    def __init__(self, app):
        self.app = app

    @classmethod
    def name(cls):
        return 'item_spike'

    def spike(self, filter, user):
        item_model = get_model(ItemModel)
        item = item_model.find_one(filter)
        if item and can_lock(item, user):
            expiry_minutes = app.settings['SPIKE_EXPIRY_MINUTES']
            # check if item is in a desk
            if "task" in item and "desk" in item["task"]:
                    # then use the desks spike_expiry
                    desk = get_resource_service('desks').find_one(_id=item["task"]["desk"], req=None)
                    expiry_minutes = desk.get('spike_expiry', expiry_minutes)

            updates = {IS_SPIKED: True, EXPIRY: get_expiry_date(expiry_minutes)}
            item_model.update(filter, updates)
            push_notification('item:spike', item=str(item.get('_id')), user=str(user))
        else:
            raise SuperdeskError("Item couldn't be spiked. It is locked by another user")
        item = item_model.find_one(filter)
        return item

    def unspike(self, filter, user):
        item_model = get_model(ItemModel)
        item = item_model.find_one(filter)
        if item:
            updates = {IS_SPIKED: None, EXPIRY: None}
            item_model.update(filter, updates)
            push_notification('item:unspike', item=str(filter.get('_id')), user=str(user))