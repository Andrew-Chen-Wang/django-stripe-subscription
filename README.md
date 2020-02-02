# Goals with Stripe + Django

This is a Stripe and Django integration "tutorial." It will walk through the subscription methods that [Stripe](https://stripe.com) offers. It will cover topics like handling subscription cycles, almost-expiration notifications, and expiration handling. Only Django is necessary (if you choose to not use a `.env` file environment).

---
### Goals

- Handle subscription payments
    - The purpose of multiple dates is to allure your customers into subscribing for a longer period of time for a cheaper price. Loyalty and user experience outweighs the loss of minuscule profit opportunity.
    - Local: 30 seconds, 1 minute, 2 minutes
    - Production: 3 days, 1 week, 1 month, 1 year, Biannual
- Handle purchase cancellations
    - Utilizes Stripe webhooks
- Handle timed event
    - 1 day before expiration, "send email"
    - On expiration, update database record

---
### Layout

- Django will provide the templates
- Backend + Django Views will handle Stripe webhooks

---
### Setup

Structure:
```
├── LICENSE
├── README.md
├── manage.py
├── public
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── vars.py
│   └── views.py
├── requirements.txt
├── stripe
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── template.env 
└── templates
```

Note: **I have disabled the AUTH_PASSWORD_VALIDATORS** to make testing easier for me.

1. Download or clone this repository. In a terminal/cmd go to the root level
2. Create a virtual environment and `pip install -r requirements.txt`
3. Run the app: `python manage.py runserver`

### Stripe setup
1. Create a Stripe. It is not necessary to have a bank account on hand right now (as of 2/1/2020).
2. You will be given 2 test API keys in the dashboard. You can also search "API Keys" in the search bar
3. Copy and paste those into a `.env` file. Your `.env` file should look similar to the `template.env` file. You can also just replace `os.getenv("STRIPE_PUBLISHABLE_KEY")` and the other var with your keys in `settings.py`.
4. Return the Stripe dashboard and go to 

---
### Notes
- Stripe billing: https://stripe.com/docs/billing/lifecycle
- Stripe subscriptions: https://stripe.com/docs/api/subscriptions/cancel
- Quick-start Django login: 