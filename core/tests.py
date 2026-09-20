from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.forms import ContactForm
from core.github import _cells_to_weeks, _parse_calendar_cells, get_contributions
from core.recaptcha import verify_recaptcha


SAMPLE_HTML = """
<table class="ContributionCalendar-grid">
  <td data-date="2025-01-05" id="contribution-day-component-0-0" data-level="0"></td>
  <td data-date="2025-01-06" id="contribution-day-component-1-0" data-level="2"></td>
  <td data-date="2025-01-12" id="contribution-day-component-0-1" data-level="1"></td>
  <td data-date="2025-01-13" id="contribution-day-component-1-1" data-level="4"></td>
</table>
<p>3 contributions on January 6th.</p>
<p>1 contribution on January 13th.</p>
"""


class GitHubContributionTests(SimpleTestCase):
    def test_parse_calendar_cells(self):
        cells = _parse_calendar_cells(SAMPLE_HTML)
        self.assertEqual(len(cells), 4)
        self.assertEqual(cells[1][3], 2)

    def test_cells_to_weeks(self):
        cells = _parse_calendar_cells(SAMPLE_HTML)
        weeks = _cells_to_weeks(cells)
        self.assertEqual(weeks[0], [0, 2])
        self.assertEqual(weeks[1], [1, 3])

    @override_settings(
        GITHUB_USERNAME="JuanPuyo1",
        GITHUB_TOKEN="",
        GITHUB_CONTRIBUTIONS_CACHE_TIMEOUT=3600,
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "tests",
            }
        },
    )
    def test_live_fetch_returns_github_source(self):
        data = get_contributions()
        self.assertEqual(data.source, "github")
        self.assertGreater(data.total, 0)
        self.assertEqual(len(data.desktop_grid), 53)
        self.assertEqual(len(data.mobile_grid), 26)


class ContactFormTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(RECAPTCHA_SECRET_KEY="test-secret")
    @patch("core.forms.verify_recaptcha", return_value=False)
    def test_rejects_missing_captcha(self, _mock_verify):
        request = self.factory.post("/contact/")
        form = ContactForm(
            {
                "name": "Esteban",
                "email": "test@example.com",
                "message": "Hello",
            },
            request=request,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("captcha", form.errors.as_text().lower())

    @override_settings(RECAPTCHA_SECRET_KEY="test-secret")
    @patch("core.forms.verify_recaptcha", return_value=True)
    def test_accepts_valid_captcha(self, mock_verify):
        request = self.factory.post(
            "/contact/",
            REMOTE_ADDR="127.0.0.1",
        )
        form = ContactForm(
            {
                "name": "Esteban",
                "email": "test@example.com",
                "message": "Hello",
                "g-recaptcha-response": "valid-token",
            },
            request=request,
        )
        self.assertTrue(form.is_valid())
        mock_verify.assert_called_once_with("valid-token", "127.0.0.1")


class RecaptchaVerificationTests(SimpleTestCase):
    @override_settings(RECAPTCHA_SECRET_KEY="test-secret", RECAPTCHA_SCORE_THRESHOLD=0.5)
    @patch("core.recaptcha.json.load", return_value={"success": True, "score": 0.9, "action": "contact"})
    @patch("core.recaptcha.urllib.request.urlopen")
    def test_accepts_valid_v3_response(self, _mock_urlopen, _mock_json):
        self.assertTrue(verify_recaptcha("token", "127.0.0.1"))

    @override_settings(RECAPTCHA_SECRET_KEY="test-secret", RECAPTCHA_SCORE_THRESHOLD=0.5)
    @patch("core.recaptcha.json.load", return_value={"success": True, "score": 0.2, "action": "contact"})
    @patch("core.recaptcha.urllib.request.urlopen")
    def test_rejects_low_score(self, _mock_urlopen, _mock_json):
        self.assertFalse(verify_recaptcha("token"))

    @override_settings(RECAPTCHA_SECRET_KEY="test-secret", RECAPTCHA_SCORE_THRESHOLD=0.5)
    @patch("core.recaptcha.json.load", return_value={"success": True, "score": 0.9, "action": "login"})
    @patch("core.recaptcha.urllib.request.urlopen")
    def test_rejects_wrong_action(self, _mock_urlopen, _mock_json):
        self.assertFalse(verify_recaptcha("token"))
