import logging
import json

from Products.Five.browser import BrowserView
from plone import api


logger = logging.getLogger('infoporto.push')


class DevicesView(BrowserView):

    def __call__(self):
        username = api.user.get_current().getUserName()
        logger.info('calling devices registrations by user %s...' % username)

        container = api.content.get(path='/devices/')

        obj = api.content.create(
            type='Device',
            title='%s' % self.request.token,
            container=container)

        api.content.transition(obj=obj, transition='submit')

        data = dict(message="devices registered")
        pretty = json.dumps(data, sort_keys=True)
        self.request.response.setHeader("Content-type", "application/json")
    
        return pretty

