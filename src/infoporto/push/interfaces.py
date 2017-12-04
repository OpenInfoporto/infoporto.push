# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from infoporto.push import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective import dexteritytextindexer
from zope.interface import implements
from zope.component import adapts
from plone import api

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from infoporto.push.helpers import PushMessage


class IInfoportoPushLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IDevice(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    dexteritytextindexer.searchable('token')    
    token = schema.Text(
        title=_(u"token"),
        required=False
    )

    platform = schema.Text(
        title=_(u"platform"),
        required=False
    )

    dexteritytextindexer.searchable('owner')
    owner = schema.TextLine(
        title=_(u"owner"),
        required=False
    )


states = SimpleVocabulary(
    [SimpleTerm(value=u'OUTGOING', title=_(u'Outgoing')),
     SimpleTerm(value=u'READ', title=_(u'Read')),
     SimpleTerm(value=u'SENT', title=_(u'Sent')),]
)


class IPushMessage(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    message = schema.Text(
        title=_(u"Message"),
        required=False,
    )

    dexteritytextindexer.searchable('recipient')
    recipient = schema.TextLine(
        title=_(u"Recipient"),
        required=True,
    )

    state = schema.Choice(
        title=_(u"state"),
        vocabulary=states,
        default='OUTGOING'
    )

    extra = schema.Text(
        title=_(u"extra"),
        default=u"{}"
    )
