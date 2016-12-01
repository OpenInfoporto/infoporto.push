import logging
import json

from zope.component import getUtility                                                                    
from plone.registry.interfaces import IRegistry

from Products.Five.browser import BrowserView
from plone import api
from infoporto.push.helpers import PushDevice, PushMessage

logger = logging.getLogger('infoporto.push')


class DevicesView(BrowserView):

    def __call__(self):
        username = api.user.get_current().getUserName()
        logger.info('calling devices registrations by user %s...' % username)

        body = self.request.get('BODY')
        body = json.loads(body)
        token = body.get('token')

        device_helper = PushDevice(token, body.get('platform'), api.user.get_current())
        device = device_helper.register()

        message = PushMessage([token], "Welcome!")
        message.send()
        logger.info("Notifications to %s added to queue" % token)

        pretty = json.dumps(dict(message="Device registered!"), sort_keys=True)
        self.request.response.setHeader("Content-type", "application/json")
    
        return pretty


class PushQueueView(BrowserView):
    
    def __call__(self):
        registry = getUtility(IRegistry)
        push_locations = registry['infoporto.push_location'] or '/push/'

        notifications = api.content.find(portal_type='PushMessage')
        
        for notification in notifications:
            notification = notification.getObject()
            pm = PushMessage([notification.recipient], notification.message).send()

        return "Clean!"

