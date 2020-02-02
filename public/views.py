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
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

import stripe
from stripe.error import SignatureVerificationError


def index(request):
    return render(request, "index.html")


# Stripe
# ----------------------------------
"""
Starting the Stripe CLI and connecting it to the webhook:
https://stripe.com/docs/stripe-cli#forward-events
Futher instructions in the stripe_webhook docstring

Creating events:
https://stripe.com/docs/stripe-cli#api-requests
"""


def base_handle_webhook(request: HttpRequest, event: stripe.Event):
    """
    THIS IS NOT A VIEW. Refer to stripe_webhook view.
    Below are the event objects.
    I advise you make a function and give it the parameters
    as above (il.e. request and event).
    """
    print(event)

    payment_intent_obj = {
        # https://stripe.com/docs/api/payment_intents/object
        "id": "pi_1DbsKl2eZvKYlo2CLVsS86l8",
        "object": "payment_intent",
        "amount": 1000,
        "amount_capturable": 0,
        "amount_received": 0,
        "application": None,
        "application_fee_amount": None,
        "canceled_at": None,
        "cancellation_reason": None,
        "capture_method": "automatic",
        "charges": {
            "object": "list",
            "data": [],
            "has_more": False,
            "url": "/v1/charges?payment_intent=pi_1DbsKl2eZvKYlo2CLVsS86l8"
        },
        "client_secret": "pi_1DbsKl2eZvKYlo2CLVsS86l8_secret_NKw0ZjWEMDt6RX4s5o7yMPF7H",
        "confirmation_method": "automatic",
        "created": 1543508747,
        "currency": "usd",
        "customer": "cus_E40L3r3Exclknq",
        "description": None,
        "invoice": None,
        "last_payment_error": None,
        "livemode": False,
        "metadata": {},
        "next_action": None,
        "on_behalf_of": None,
        "payment_method": None,
        "payment_method_options": {},
        "payment_method_types": [
            "card"
        ],
        "receipt_email": None,
        "review": None,
        "setup_future_usage": None,
        "shipping": None,
        "statement_descriptor": None,
        "statement_descriptor_suffix": None,
        "status": "requires_payment_method",
        "transfer_data": None,
        "transfer_group": None
    }

    payment_method_obj = {
        # https://stripe.com/docs/api/payment_methods/object
        "id": "pm_123456789",
        "object": "payment_method",
        "billing_details": {
            "address": {
                "city": None,
                "country": None,
                "line1": None,
                "line2": None,
                "postal_code": "94103",
                "state": None
            },
            "email": "jenny@example.com",
            "name": None,
            "phone": "+15555555555"
        },
        "card": {
            "brand": "visa",
            "checks": {
                "address_line1_check": None,
                "address_postal_code_check": None,
                "cvc_check": None
            },
            "country": "US",
            "exp_month": 8,
            "exp_year": 2021,
            "fingerprint": "Xt5EWLLDS7FJjR1c",
            "funding": "credit",
            "generated_from": None,
            "last4": "4242",
            "three_d_secure_usage": {
                "supported": True
            },
            "wallet": None
        },
        "created": 123456789,
        "customer": None,
        "livemode": False,
        "metadata": {
            "order_id": "123456789"
        },
        "type": "card"
    }


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
    So here's their GUI that monitors events: https://github.com/stripe/stripe-webhook-monitor

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
    except SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the DIFFERENT events
    # When customizing, I recommend you be modular with this:
    # Create several different functions with the params: request and event.
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
    # In case you wanted a GUI monitoring events: https://github.com/stripe/stripe-webhook-monitor
    # since, with the stripe-cli, you won't be able to see test events in the Dashboard.
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
