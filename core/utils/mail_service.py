from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

context = {

}
html_message = render_to_string('email-forget-pass.html', context)

# Plain text version for email clients that don't support HTML
plain_message = strip_tags(html_message)


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
