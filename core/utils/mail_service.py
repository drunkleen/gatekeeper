from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.models import UserAccount
from GateKeeper.settings import EMAIL_HOST_USER


def send_email():
    subject = 'Subject Here'
    message = 'Message Here'
    from_email = 'mail@gmail.com'
    recipient_list = ["to@gmail.com"]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False
    )


def send_forget_password_email(request, user: UserAccount, reset_key: str):

    subject = 'GateKeeper | Password Reset Request'
    reset_link = f'{request.scheme}://{request.get_host()}/auth/reset-password/{reset_key}'
    plain_message = f"Dear {user.first_name},\n\nIt appears that you've forgotten your password. No need to worry – we've got you covered!\n\nPlease click on the link below to reset your password:\n{reset_link}\n\nThank you for choosing [Your Website/Application Name]. We appreciate your understanding and cooperation.\n\nBest regards,\nSupport Team"

    context = {
        'user': user,
        'reset_link': reset_link
    }
    email_html_message = render_to_string('login/email-forget-pass.html', context)

    send_mail(
        subject,
        plain_message,
        EMAIL_HOST_USER,
        [user.email],
        html_message=email_html_message,
        fail_silently=True
    )

