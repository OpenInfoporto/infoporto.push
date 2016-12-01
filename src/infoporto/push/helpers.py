from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone import api 
from pyfcm import FCMNotification
import logging

logger = logging.getLogger(__name__)


class PushMessage:

    def __init__(self, token_list, title, body=None, badge=None):
        self.token_list = token_list
        self.title = title
        self.body = body
        self.badge = badge
        
        registry = getUtility(IRegistry)
        self.push_service = FCMNotification(api_key=registry['infoporto.push_api_key'])
        logger.debug(registry['infoporto.push_api_key'])

    def send(self):
        logger.info("Sending push to %s" % self.token_list)
        result = self.push_service.notify_multiple_devices(registration_ids=self.token_list, 
                                                           message_title=self.title, 
                                                           message_body=self.body)
        logger.debug(result)

    def queue(self):
        
        container = api.content.get(path='/push')

        for token in self.token_list:
            obj = api.content.create(
                    type='PushMessage',
                    title=self.title,
                    message=self.body,
                    recipient=token,
                    state='OUTGOING',
                    container=container)

            logger.info("Push %s for %s added to queue" % (obj.id, token))

