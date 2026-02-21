from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
import os


def Home(request):
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'home/index.html', context)


def health_check(request):
    """Health check endpoint for debugging deployment"""
    return JsonResponse({
        'status': 'ok',
        'debug': settings.DEBUG,
        'environment': os.getenv('ENVIRONMENT', 'not set'),
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'database': settings.DATABASES['default']['ENGINE'].split('.')[-1],
    })