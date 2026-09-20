from django.conf import settings


def recaptcha(request):
    return {
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
    }


def site(request):
    return {
        "google_analytics_id": settings.GOOGLE_ANALYTICS_ID,
    }
