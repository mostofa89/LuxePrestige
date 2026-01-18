from django.http import HttpResponse
from django.shortcuts import render
from accounts.models import Profile


def Home(request):
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'home/index.html', context)