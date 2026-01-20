from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    membership_choice = [
        ('B', 'Bronze'),
        ('S', 'Silver'),
        ('G', 'Gold'),
        ('P', 'Platinum'),

    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='profiles/', blank=True, null=True)
    membership_choice = models.CharField(max_length=1, choices=membership_choice, default='B')
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} {self.address_line}, {self.city}, {self.state}, {self.country} - {self.postal_code}"
    
    
    

