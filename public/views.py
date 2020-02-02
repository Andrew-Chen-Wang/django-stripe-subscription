"""
What does stripe handle? Stripe's webhooks will send a bunch of information
that you have signed up for in the Stripe Developer/Webhook section.
That can be found here: https://dashboard.stripe.com/test/webhooks when you are logged-in

Follow the README closely in order for this to work. Obviously, these are just the base methods
that you will need to expand on for your usage.
"""
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, "index.html")


def stripe_webhook(request):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))


# Authentication: Django's default authentication
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#all-authentication-views

def register(request):
    """Using Django's pre-made UserCreationForm"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        else:
            form = UserCreationForm()
            return render(request, "registration/register.html", {"form": form})
    else:
        form = UserCreationForm()
        return render(request, "registration/register.html", {"form": form})
