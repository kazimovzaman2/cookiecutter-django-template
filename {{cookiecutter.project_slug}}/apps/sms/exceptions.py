from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class SmsServiceException(APIException):
    """Api exception indicating error from sms service."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Error from sms service.")
    default_code = "sms_service_error"


class InvalidPhoneNumberException(APIException):
    """Api exception indicating invalid phone number."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"phone_number": _("Phone number is invalid.")}
    default_code = "invalid_phone_number"
