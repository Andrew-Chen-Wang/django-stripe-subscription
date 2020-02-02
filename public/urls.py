from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Stripe

    # Authentication
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.register, name="register")
]
