import logging
import json

from pyfcm.errors import AuthenticationError
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

        try:
            message = PushMessage([token], "Welcome!", "Welcome body!")
            message.send()
            logger.info("Notifications to %s added to queue" % token)

            response = json.dumps(dict(message="Device registered!"), sort_keys=True)
            self.request.response.setHeader("Content-type", "application/json")
        except AuthenticationError, e:
            logger.error(e)
            response = json.dumps(dict(message="Error sending welcome notification"))

        return response


class PushTestView(BrowserView):

    def __call__(self):
        username = api.user.get_current().getUserName()

        body = self.request.get('BODY')
        body = json.loads(body)
        recipient_user = body.get('recipient')

        logger.info('calling test push by user %s to user %s...' % (username, recipient_user))

        data_message = dict(UID="66fa7286ebb2488e9f94644f95c81e96")

        message = PushMessage([], "titolo", "Testmaela", data_message=data_message)
        message.set_recipient(recipient_user)

        try:
            message.send()
        except Exception, e:
            logger.error(e)
            return json.dumps(dict(message=e))

        return json.dumps(dict(message="Message sent to %s." % message.token_list))


class PushQueueView(BrowserView):
    
    def __call__(self):
        registry = getUtility(IRegistry)
        push_locations = registry['infoporto.push_location'] or '/push/'

        notifications = api.content.find(portal_type='PushMessage')
        
        for notification in notifications:
            notification = notification.getObject()
            pm = PushMessage([notification.recipient], notification.message).send()

        return "Clean!"

