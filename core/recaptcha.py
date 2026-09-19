"""Google reCAPTCHA v2 verification."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)

VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


def verify_recaptcha(token: str, remote_ip: str | None = None) -> bool:
    secret = settings.RECAPTCHA_SECRET_KEY
    if not secret:
        logger.error("RECAPTCHA_SECRET_KEY is not configured")
        return False

    if not token:
        return False

    payload = urllib.parse.urlencode(
        {
            "secret": secret,
            "response": token,
            **({"remoteip": remote_ip} if remote_ip else {}),
        }
    ).encode()

    request = urllib.request.Request(
        VERIFY_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        logger.exception("reCAPTCHA verification request failed")
        return False

    return bool(result.get("success"))
