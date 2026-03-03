import secrets
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User
from .models import EmailOTP
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta

def generate_otp(email, username=None):
    # Delete any existing OTPs for this email
    EmailOTP.objects.filter(email=email).delete()

    otp = str(secrets.randbelow(900000) + 100000)  # Cryptographically secure
    EmailOTP.objects.create(email=email, code=otp)
    if not username:
        user = User.objects.filter(email=email).first()
        username = user.username if user else email.split('@')[0]

    subject = 'Your OTP Code'
    message = (
        f"""Dear {username},

Thank you for your request.

Your verification code is: {otp}

Please use this code to complete your verification process. This code is valid for a limited time only. Do not share this code with anyone for security reasons.

If you did not request this code, please ignore this email.

Best regards,
LUXURY STORE Team
"""
    )

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        cc=getattr(settings, 'EMAIL_CC', []),
        bcc=getattr(settings, 'EMAIL_BCC', []),
    )

    try:
        email_message.send(fail_silently=False)
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return None  # Signal that sending failed

    return otp


def verify_otp(email, otp_entered):
    try:
        otp_record = EmailOTP.objects.filter(email=email).latest('created_at')
    except EmailOTP.DoesNotExist:
        return False, "No OTP found for this email."

    # Check expiry (10 minutes)
    expiry_time = otp_record.created_at + timedelta(minutes=10)
    if timezone.now() > expiry_time:
        otp_record.delete()
        return False, "OTP has expired. Please request a new one."

    if otp_record.code != otp_entered:
        return False, "Invalid OTP."

    # OTP is valid — delete it so it can't be reused
    otp_record.delete()
    return True, "OTP verified successfully."


def send_verification_confirmation_email(email, username=None):
    if not username:
        user = User.objects.filter(email=email).first()
        username = user.username if user else email.split('@')[0]

    subject = 'Email Verified Successfully'
    message = (
        f"""Dear {username},

Your email has been verified successfully.

Your account setup is now complete, and you can log in to continue.

If this was not you, please contact support immediately.

Best regards,
LUXURY STORE Team
"""
    )

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        cc=getattr(settings, 'EMAIL_CC', []),
        bcc=getattr(settings, 'EMAIL_BCC', []),
    )

    try:
        email_message.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending verification confirmation email: {e}")
        return False


def send_templated_mail(mail_to, mail_cc, mail_bcc, subject, template, context):
    mail_to_set = set(mail_to) if mail_to else set()
    mail_cc_set = set(mail_cc) if mail_cc else set()
    common_emails = mail_to_set.intersection(mail_cc_set)

    mail_cc_set -= common_emails

    html_body = render_to_string(template, context)
    text_body = strip_tags(html_body)

    if mail_to_set:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=list(mail_to_set),
            cc=list(mail_cc_set),
            bcc=list(mail_bcc) if mail_bcc else [],
        )

        email.attach_alternative(html_body, "text/html")
        try:
            email.send(fail_silently=False)

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

        return True

    return False