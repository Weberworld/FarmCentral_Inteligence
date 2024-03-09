import os
from django.core.mail import send_mail


def send_email(subject, message, recipient_email):
    """
    Overrides the default django send_mail function
    """
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[recipient_email],
        from_email=os.environ.get("EMAIL_USERNAME"),
        fail_silently=False
    )
