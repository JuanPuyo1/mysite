from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("partials/contributions/", views.contributions_partial, name="contributions"),
    path("contact/", views.contact_submit, name="contact"),
]
