"""Google reCAPTCHA v3 verification."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)

VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


def verify_recaptcha(
    token: str,
    remote_ip: str | None = None,
    *,
    expected_action: str = "contact",
) -> bool:
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

    if not result.get("success"):
        logger.warning("reCAPTCHA verification rejected: %s", result.get("error-codes"))
        return False

    score = result.get("score")
    if score is None or score < settings.RECAPTCHA_SCORE_THRESHOLD:
        logger.warning("reCAPTCHA score too low: %s", score)
        return False

    action = result.get("action")
    if action != expected_action:
        logger.warning("reCAPTCHA action mismatch: expected %s, got %s", expected_action, action)
        return False

    return True
