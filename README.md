# infoporto.push
Plone add-on to handle mobile devices and send push notifications via GCM

USAGE
=====

Configure your Firebase Cloud Messagging API key in Plone registry ::

    infoporto push_api_key


Register mobile clients calling - after authentication - the custom action using POST passing token as parameter ::

    http://hostname/@@devices
