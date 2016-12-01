import logging
import json

from Products.Five.browser import BrowserView
from plone import api
from infoporto.push.helpers import PushMessage

logger = logging.getLogger('infoporto.push')


class DevicesView(BrowserView):

    def __call__(self):
        username = api.user.get_current().getUserName()
        logger.info('calling devices registrations by user %s...' % username)

        container = api.content.get(path='/devices/')
        
        existings = api.content.find(portal_type='Device', Title=self.request.token)
        
        if existings:
            logger.warning("Found %s devices with same token... deleting... " % len(existings))
            api.content.delete(objects=[o.getObject() for o in existings])

        obj = api.content.create(
            type='Device',
            title='%s' % self.request.token,
            token=self.request.token,
            platform=self.request.platform,
            user=api.user.get_current(),
            container=container)
        api.content.transition(obj=obj, transition='submit')

        data = dict(message="devices registered")
        message = PushMessage([self.request.token], "Welcome!")
        message.queue()
        pretty = json.dumps(data, sort_keys=True)
        self.request.response.setHeader("Content-type", "application/json")
    
        return pretty

