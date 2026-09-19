from django import forms
from django.core.exceptions import ValidationError

from .recaptcha import verify_recaptcha

INPUT_CLASS = (
    "input input-bordered w-full rounded-lg border-line bg-bg px-3 py-3 text-sm "
    "text-ink placeholder:text-muted focus:border-accent focus:outline-none "
    "lg:h-12 lg:bg-surface lg:px-4 lg:py-3.5 lg:text-[15px]"
)

TEXTAREA_CLASS = (
    "textarea textarea-bordered h-[88px] w-full resize-none rounded-lg border-line "
    "bg-bg px-3 py-3 text-sm text-ink placeholder:text-muted focus:border-accent "
    "focus:outline-none lg:h-[120px] lg:bg-surface lg:px-4 lg:py-3.5 lg:text-[15px]"
)


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "Your name",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "you@email.com",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": TEXTAREA_CLASS,
                "placeholder": "What are you working on?",
                "rows": 3,
            }
        ),
    )

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        token = self.data.get("g-recaptcha-response", "")
        remote_ip = None
        if self.request:
            remote_ip = self.request.META.get("REMOTE_ADDR")

        if not verify_recaptcha(token, remote_ip):
            raise ValidationError("Please complete the captcha verification.")

        return cleaned_data
