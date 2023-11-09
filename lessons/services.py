import stripe

from lms.settings import STRIPE_SECRET_KEY


def get_stripe_session(course, user, payment_amount):
    stripe.api_key = STRIPE_SECRET_KEY
    product_for_stripe = stripe.Product.create(name=course.title)

    price_for_stripe = stripe.Price.create(
        unit_amount=payment_amount * 100,  # todo - change model for price
        currency="usd",
        product=f"{product_for_stripe.id}",
    )
    session_for_stripe = stripe.checkout.Session.create(
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': f'{price_for_stripe.id}',
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://mydomain.success/',
        cancel_url='http://mydomain.cancel/',
        customer_email=f'{user.email}'
    )
    return session_for_stripe


def get_session_by_stripe_id(stripe_id) -> dict:
    """ return session from stripe API"""
    stripe.api_key = STRIPE_SECRET_KEY
    return stripe.checkout.Session.retrieve(stripe_id)
