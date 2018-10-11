from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone import api 
from pyfcm import FCMNotification

import json
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
        user_devices = api.content.find(portal_type='Device', owner=self.user.id, platform=self.platform, container=container)
        logger.debug(user_devices)
        api.user.grant_roles(user=self.user, obj=container, roles=['Manager'])
        for d in user_devices:
            device = d.getObject()
            if device.owner == self.user.id:
                logger.info('deleting device {}'.format(device.id))
                api.content.delete(objects=[device])

        #api.content.delete(objects=[o.getObject() for o in user_device])

        obj = api.content.create(
            type='Device',
            title="%s device (%s)" % (self.user.id, self.platform),
            token=self.token,
            owner=self.user.id,
            platform=self.platform,
            container=container)

        obj.reindexObject()


        api.content.transition(obj=obj, transition='submit')

        return obj


class PushMessage:

    def __init__(self, token_list, title, body=None, badge=None, data_message=None, extra_kwargs=None):
        self.token_list = token_list
        self.title = title
        self.body = body
        self.badge = badge
        self.data_message = data_message or dict()
        self.extra_kwargs = extra_kwargs
        self.username = None

        self.data_message.update(dict(click_action='FLUTTER_NOTIFICATION_CLICK'))
        
        registry = getUtility(IRegistry)
        self.push_service = FCMNotification(api_key=registry['infoporto.push_api_key'])
        self.push_locations = registry['infoporto.push_location'] or '/push/'

    def send(self):
        logger.info("Sending push to %s" % self.token_list)
        logger.info("Title: %s Badge: %s User: %s" % (self.title, self.badge, self.username))
        logger.info(self.extra_kwargs)

        if not self.title:
            result = self.push_service.notify_multiple_devices(registration_ids=self.token_list, badge=self.badge, content_available=False, extra_kwargs=self.extra_kwargs, data_message=self.data_message)
        else:
            result = self.push_service.notify_multiple_devices(registration_ids=self.token_list, 
                                                               message_title=self.title, 
                                                               message_body=self.title,
                                                               data_message=self.data_message,
                                                               badge=self.badge,
                                                               sound='Default',
                                                               content_available=True)

        logger.debug(result)

    def queue(self):
        container = api.content.get(path=self.push_locations)

        for token in self.token_list:
            obj = api.content.create(
                    type='PushMessage',
                    title=self.title,
                    message=self.body,
                    recipient=token,
                    state='OUTGOING',
                    extra=json.dumps(self.data_message),
                    container=container)
            logger.info("granting role for %s to user %s " % (obj.title, self.username))
            api.user.grant_roles(username=self.username, obj=obj, roles=['Reader'])
            obj.reindexObject()
            logger.info("Push %s for %s added to queue" % (obj.id, token))

    def set_recipient(self, username, platform=None):
        registry = getUtility(IRegistry)
        self.username = username
        container = api.content.get(path=registry['infoporto.devices_location'])
        if platform:
            devices = api.content.find(portal_type='Device', owner=username, container=container, platform=platform)
        else:
            devices = api.content.find(portal_type='Device', owner=username, container=container)        

        logger.debug("Found %s devices for user %s" % (len(devices), username))
        self.token_list = list()
        for d in devices:
            d = d.getObject()
            if d.owner == username: self.token_list.append(d.token)
        #self.token_list = [d.getObject().token for d in devices]

