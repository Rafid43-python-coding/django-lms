from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    send_mail(
        subject="Welcome to LMS",
        message=f"Hello {user.username},\n\nWelcome to our Learning Management System. Happy Learning!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )