from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile, Address, OTP
import random


# =========================
# AUTH VIEWS
# =========================

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# =========================
# REGISTRATION + OTP
# =========================

def RegisterView(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        username   = request.POST.get('username')
        email      = request.POST.get('email')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('accounts:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('accounts:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('accounts:register')

        # Store temp data in session
        request.session['registration_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password1,
        }

        # Invalidate previous OTPs
        OTP.objects.filter(email=email, is_used=False).update(is_used=True)

        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(
            email=email,
            otp=otp_code,
            expiry_time=timezone.now() + timedelta(minutes=10)
        )

        # Send email
        try:
            send_mail(
                subject='Verify Your Email',
                  message = f"""
Hello {first_name},

Thank you for registering at Ecommerce Store!

Your verification code is: {otp_code}

This code is valid for 10 minutes. Please enter it in the verification page to complete your registration.

If you did not request this, please ignore this email.

Best regards,
The Ecommerce Store Team
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent to your email")
        except Exception as e:
            if settings.DEBUG:
                print(f"OTP for {email}: {otp_code}")
            messages.warning(request, "Email failed. OTP printed in console.")

        return redirect('accounts:verify_otp')

    return render(request, 'accounts/register.html')


def verify_otp_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        data = request.session.get('registration_data')

        if not data:
            messages.error(request, "Session expired. Register again.")
            return redirect('accounts:register')

        try:
            otp_entry = OTP.objects.get(
                email=data['email'],
                otp=otp,
                is_used=False,
                expiry_time__gt=timezone.now()
            )

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )

            otp_entry.is_used = True
            otp_entry.save()

            Profile.objects.create(user=user)

            del request.session['registration_data']

            messages.success(request, "Registration successful. Please login.")
            return redirect('accounts:login')

        except OTP.DoesNotExist:
            messages.error(request, "Invalid or expired OTP")

    return render(request, 'accounts/verify_otp.html')


def resend_otp_view(request):
    data = request.session.get('registration_data')

    if not data:
        messages.error(request, "Session expired. Register again.")
        return redirect('accounts:register')

    OTP.objects.filter(email=data['email'], is_used=False).update(is_used=True)

    otp_code = str(random.randint(100000, 999999))
    OTP.objects.create(
        email=data['email'],
        otp=otp_code,
        expiry_time=timezone.now() + timedelta(minutes=10)
    )

    try:
        send_mail(
            subject='Resend OTP',
            message=f"Your new OTP is {otp_code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data['email']],
            fail_silently=False,
        )
        messages.success(request, "New OTP sent")
    except Exception:
        if settings.DEBUG:
            print(f"Resent OTP: {otp_code}")
        messages.warning(request, "Email failed. OTP printed in console.")

    return redirect('accounts:verify_otp')


# =========================
# PROFILE & ADDRESS
# =========================

@login_required(login_url='accounts:login')
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required(login_url='accounts:login')
def address_view(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            country=request.POST.get('country'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            address_line=request.POST.get('address_line'),
        )
        messages.success(request, "Address added successfully")
        return redirect('accounts:profile')

    return render(request, 'accounts/address.html')
