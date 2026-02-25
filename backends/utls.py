import random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import EmailOTP
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    EmailOTP.objects.create(email=email, otp=otp)

    subject = 'Your OTP code'
    message = (
        f'Your OTP code is {otp}.\n\n'
        'This code expires in 10 minutes.'
    )

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        cc=getattr(settings, 'EMAIL_CC', []),
        bcc=getattr(settings, 'EMAIL_BCC', []),
    )
    email_message.send(fail_silently=False)

    return otp


def send_templated_mail(mail_to, mail_cc, mail_bcc, subject, template, context):
    mail_to_set = set(mail_to) if mail_to else set()
    mail_cc_set = set(mail_cc) if mail_cc else set()
    common_emails = mail_to_set.intersection(mail_cc_set)

    mail_cc_set -= common_emails

    html_body = render_to_string(template, context)
    text_body = strip_tags(html_body)

    if mail_to_set:
        email = EmailMultiAlternatives(
            subject = subject,
            body = text_body,
            from_email = settings.DEFAULT_FROM_EMAIL,
            to = list(mail_to_set),
            cc = list(mail_cc_set),
            bcc = list(mail_bcc) if mail_bcc else [],

        )

        email.attach_alternative(html_body, "text/html")
        try:
            email.send(fail_silently=False)

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

        return True

    return False
            