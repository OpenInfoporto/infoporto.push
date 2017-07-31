from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone import api 
from pyfcm import FCMNotification
import logging

logger = logging.getLogger(__name__)


class PushDevice:

    def __init__(self, token, platform, user):
        self.token = token
        self.platform = platform
        self.user = user

        registry = getUtility(IRegistry)
        self.device_location = registry['infoporto.devices_location']

    def register(self):
        container = api.content.get(path=self.device_location)
        api.content.delete(objects=[o.getObject() for o in api.content.find(portal_type='Device',
                                                                            owner=self.user.id,
                                                                            container=container)])

        obj = api.content.create(
            type='Device',
            title="%s device (%s)" % (self.user.id, self.platform),
            token=self.token,
            owner=self.user.id,
            platform=self.platform,
            container=container)

        api.content.transition(obj=obj, transition='submit')

        return obj


class PushMessage:

    def __init__(self, token_list, title, body=None, badge=None):
        self.token_list = token_list
        self.title = title
        self.body = body
        self.badge = badge
        
        registry = getUtility(IRegistry)
        self.push_service = FCMNotification(api_key=registry['infoporto.push_api_key'])
        self.push_locations = registry['infoporto.push_location'] or '/push/'

    def send(self):
        logger.info("Sending push to %s" % self.token_list)
        result = self.push_service.notify_multiple_devices(registration_ids=self.token_list, 
                                                           message_title=self.title, 
                                                           message_body=self.body)
        logger.debug(result)

    def queue(self):
        print self.push_locations
        container = api.content.get(path=self.push_locations)

        for token in self.token_list:
            obj = api.content.create(
                    type='PushMessage',
                    title=self.title,
                    message=self.body,
                    recipient=token,
                    state='OUTGOING',
                    container=container)

            logger.info("Push %s for %s added to queue" % (obj.id, token))

    def set_recipient(self, username):
        registry = getUtility(IRegistry)
        container = api.content.get(path=registry['infoporto.devices_location'])
        devices = api.content.find(portal_type='Device', owner=username, container=container)
        self.token_list = [d.getObject().token for d in devices]

