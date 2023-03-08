import requests

from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_feedback_email(feedback, feedback_author_email):
    send_mail(
        'Feedback',
        f'{feedback}',
        f'{feedback_author_email}',
        ['to@example.com'],
        fail_silently=False
    )


@shared_task()
def post_created_email(email_text):
    send_mail(
        'New Post Created',
        email_text,
        'server@noreply.com',
        ['admin@noreply.com'],
        fail_silently=False
    )
