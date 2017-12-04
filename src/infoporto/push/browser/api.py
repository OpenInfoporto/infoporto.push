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

        data_message = dict(UID="9b5a8a97c8674a96804991ec1ce207d5")
        extra_kwargs = {
            'content_available': True
        }

        message = PushMessage([], "titolo", "Testmaela", data_message=data_message, extra_kwargs=extra_kwargs)
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

        #import pdb; pdb.set_trace()
        notifications = api.content.find(portal_type='PushMessage', state='OUTGOING')
        
        for notification in notifications:
            notification = notification.getObject()
            # TODO: check and remove
            if notification.state == 'OUTGOING':
                logger.debug(notification.extra)
                pm = PushMessage([notification.recipient], notification.message, data_message=json.loads(notification.extra)).send()

                notification.state = "SENT"


        return "Clean!"


class ReadNotification(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        registry = getUtility(IRegistry)
        username = api.user.get_current().getUserName()
        uuid = self.request.form["uuid"]
        push_locations = registry['infoporto.push_location'] or '/push/'

        document = api.content.get(UID=uuid)
        original = api.content.get(UID=document.original_doc)
        container = api.content.get(path="/".join(original.getPhysicalPath()))

        obj = api.content.create(
            type='DMReadingConfirm',
            title='%s-%s' % (username, document.title),
            message="Conferma di lettura da %s per il documento %s del %s" % (username, document.title, original.creation_date),
            container=container
        )
        obj.reindexObject()

        notifications = api.content.find(portal_type='PushMessage', 
                                         title=document.title)

        for n in notifications:
            if document.UID() == json.loads(n.getObject().extra).get('UID'):
                n.getObject().state = 'READ'
                n.getObject().reindexObject()
                logger.info("Setting notification %s for document %s to READ" % (n.Title, document.Title))
                   
        return "Read"

