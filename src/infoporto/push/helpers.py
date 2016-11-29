from pyfcm import FCMNotification
import logging


logger = logging.getLogger(__name__)


class PushMessage:

    def __init__(self, token_list, title, body=None, badge=None):
        self.token_list = token_list
        self.title = title
        self.body = body
        self.badge = badge
        FCM_API_KEY = ""
        push_service = FCMNotification(api_key=FCM_API_KEY)

    def send(self):
        result = self.push_service.notify_multiple_devices(registration_ids=registration_ids, 
                                                           message_title=message_title, 
                                                           message_body=message_body)
        logger.debug(result)

