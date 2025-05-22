from django.conf import settings
from django.utils.module_loading import import_string

from apps.sms.backends import BaseSmsSender

sms_sender: BaseSmsSender = import_string(settings.SMS_SENDER["BACKEND"])(
    **settings.SMS_SENDER.get("OPTIONS", {})
)
