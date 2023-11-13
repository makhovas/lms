import json
from datetime import datetime, timedelta

import stripe
from django_celery_beat.models import IntervalSchedule, PeriodicTask

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


# def set_schedule(*args, **kwargs):
#     schedule, created = IntervalSchedule.objects.get_or_create(
#         every=10,
#         period=IntervalSchedule.SECONDS,
#     )
#     PeriodicTask.objects.create(
#         interval=schedule,  # we created this above.
#         name='send email about update',  # simply describes this periodic task.
#         task='lessons.tasks.send_email_course_updated',  # name of task.
#         args=json.dumps(['arg1', 'arg2']),
#         kwargs=json.dumps({
#             'be_careful': True,
#         }),
#         expires=datetime.utcnow() + timedelta(seconds=30)
#     )
