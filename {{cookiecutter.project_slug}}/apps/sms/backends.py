"""Sms service backends."""

import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, TypedDict

import requests

from apps.sms.exceptions import (
    InvalidPhoneNumberException,
    SmsServiceException,
)

logger = logging.getLogger(__name__)


class SmsPayload(TypedDict):
    """SMS payload that is sent to the phone number.
    Must be used only for testing purposes."""

    phone_number: str
    message: str


class BaseSmsSender(ABC):
    @abstractmethod
    def send(self, phone_number: str, message: str) -> None: ...


@dataclass
class SmsSender(BaseSmsSender):
    """
    LSIM implementation of SMS sender.

    See LSIM docs: https://apps.lsim.az/quicksms/v1/smssender
    """

    login: str
    password: str
    sender: str
    send_url: ClassVar[str] = "https://apps.lsim.az/quicksms/v1/smssender"
    timeout: ClassVar[int] = 10
    client_error_codes: ClassVar[tuple[str, ...]] = (
        "WRONG_NUMBER_FORMAT",
        "NUMBER_IN_BLACK_LIST",
    )

    def _get_key(self, phone_number: str, message: str) -> str:
        return hashlib.md5(
            (
                hashlib.md5(self.password.encode()).hexdigest()
                + self.login
                + message
                + phone_number
                + self.sender
            ).encode()
        ).hexdigest()

    def send(self, phone_number: str, message: str) -> None:
        logger.info(f"Sending SMS to {phone_number} with message: {message}")
        phone_number = phone_number.replace("+", "")
        payload = {
            "login": self.login,
            "key": self._get_key(phone_number, message),
            "msisdn": phone_number,
            "text": message,
            "sender": self.sender,
            "unicode": True,
        }
        body = requests.post(self.send_url, json=payload, timeout=self.timeout).json()

        if error_message := body.get("errorMessage"):
            error_code = body.get("errorCode")

            if error_code in self.client_error_codes:
                raise InvalidPhoneNumberException

            raise SmsServiceException(
                detail=(
                    f"Failed to send SMS to {phone_number} "
                    f"with message: {message}. "
                    f"Error message: {error_message}, "
                    f"error code: {error_code}."
                )
            )


class DummySmsSender(BaseSmsSender):
    """Dummy SMS sender that just prints the message to the console.
    Can be used for testing purposes."""

    def send(self, phone_number: str, message: str) -> None:
        print(f"Sending SMS to {phone_number} with message: {message}")
