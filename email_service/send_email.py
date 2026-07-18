from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    subject = "Welcome to LMS"

    message = f"""
Hi {user.username},

Welcome to our Learning Management System!

Your account has been created successfully.

Happy Learning!

Regards,
LMS Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
