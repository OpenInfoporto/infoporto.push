import logging
import json

from Products.Five.browser import BrowserView
from plone import api
from infoporto.push.helpers import PushDevice, PushMessage

logger = logging.getLogger('infoporto.push')


class DevicesView(BrowserView):

    def __call__(self):
        username = api.user.get_current().getUserName()
        logger.info('calling devices registrations by user %s...' % username)

        device_helper = PushDevice(self.request.token, self.request.platform, api.user.get_current())
        device = device_helper.register()

        message = PushMessage([self.request.token], "Welcome!")
        message.queue()
        logger.info("Notifications to %s added to queue" % self.request.token)

        pretty = json.dumps(dict(message="Device registered!"), sort_keys=True)
        self.request.response.setHeader("Content-type", "application/json")
    
        return pretty

