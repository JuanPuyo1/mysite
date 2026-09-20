from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .data import CONTACT, EXPERIENCE, NORT, STUDIES
from .forms import ContactForm
from .github import get_contributions


def _contribution_context():
    contributions = get_contributions()
    return {
        "contribution_total": f"{contributions.total:,}",
        "desktop_grid": contributions.desktop_grid,
        "mobile_grid": contributions.mobile_grid,
        "contributions_live": contributions.source == "github",
        "github_username": contributions.username,
    }


def home(request):
    return render(
        request,
        "core/home.html",
        {
            "form": ContactForm(request=request),
            "experience": EXPERIENCE,
            "studies": STUDIES,
            "nort": NORT,
            "contact": CONTACT,
            **_contribution_context(),
        },
    )


def contributions_partial(request):
    return render(
        request,
        "core/partials/contributions_panel.html",
        _contribution_context(),
    )


@require_http_methods(["POST"])
def contact_submit(request):
    form = ContactForm(request.POST, request=request)
    if form.is_valid():
        EmailMessage(
            subject=f"Portfolio contact from {form.cleaned_data['name']}",
            body=(
                f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                f"{form.cleaned_data['message']}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_RECIPIENT_EMAIL],
            reply_to=[form.cleaned_data["email"]],
        ).send(fail_silently=False)
        if request.headers.get("HX-Request"):
            return render(request, "core/partials/contact_success.html")
        return render(
            request,
            "core/home.html",
            {
                "form": ContactForm(request=request),
                "experience": EXPERIENCE,
                "studies": STUDIES,
                "nort": NORT,
                "contact": CONTACT,
                "contact_sent": True,
                **_contribution_context(),
            },
        )

    if request.headers.get("HX-Request"):
        return render(
            request,
            "core/partials/contact_form.html",
            {"form": form, "contact": CONTACT},
            status=422,
        )
    return render(
        request,
        "core/home.html",
        {
            "form": form,
            "experience": EXPERIENCE,
            "studies": STUDIES,
            "nort": NORT,
            "contact": CONTACT,
            **_contribution_context(),
        },
        status=422,
    )
