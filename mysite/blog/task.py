import requests

from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_feedback_email(feedback, feedback_author_email):
    send_mail(
        'Feedback',
        feedback,
        [feedback_author_email],
        ['to@example.com'],
        fail_silently=False
    )
