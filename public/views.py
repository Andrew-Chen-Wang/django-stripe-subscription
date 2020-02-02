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
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import stripe


def index(request):
    return render(request, "index.html")


# Stripe
# ----------------------------------
@require_http_methods(["POST"])
@csrf_exempt
def stripe_webhook(request):
    """
    Mostly modeled after Stripe's Flask app. Flask is a minimal Django and very similar, so it's easy to read:
    https://github.com/stripe-samples/checkout-single-subscription/blob/master/client-and-server/server/python/server.py

    You also need to setup the stripe-cli since this setup uses Server+Client integration of Stripe.
    https://stripe.com/docs/stripe-cli
    Simply skip Step 3.
    Note: responses from your server are not returned to Stripe and won’t show up in the Dashboard.

    This view also verifies that it's Stripe sending us the webhook.
    https://stripe.com/docs/webhooks/signatures

    Make sure you have the stripe package installed (should be in requirements.txt)
    https://github.com/stripe/stripe-python
    """
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the DIFFERENT events
    # In case you wanted a GUI monitoring events: https://github.com/stripe/stripe-webhook-monitor
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        # contains a stripe.PaymentIntent: https://stripe.com/docs/api/payment_intents/object
        print("PaymentIntent was successful!")
    elif event.type == "payment_method.attached":
        payment_method = event.data.object
        # contains a stripe.PaymentMethod https://stripe.com/docs/api/payment_methods/object
        print("PaymentMethod was attached to a Customer")
    else:
        return HttpResponse(status=400)
    return HttpResponse(status=200)


# Authentication
# ---------------------------------------------------
# Django's default authentication
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
    form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
