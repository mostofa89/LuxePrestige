from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as message


def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message.error(request, "Invalid username or password.")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


def RegisterView(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_pic = request.FILES.get('profile_pic')

        if password1 != password2:
            message.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            message.error(request, "Username already exists.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            message.error(request, "Email already exists.")
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )

        Profile.objects.create(
            user=user,
            profile=profile_pic
        )

        message.success(request, "Account created successfully. Please sign in.")
        return redirect('login')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')