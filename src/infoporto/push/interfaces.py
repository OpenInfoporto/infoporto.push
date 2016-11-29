# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from infoporto.push import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


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

    token = schema.Text(
        title=_(u"token"),
        required=False
    )

    platform = schema.Text(
        title=_(u"platform"),
        required=False
    )

