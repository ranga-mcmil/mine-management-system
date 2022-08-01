from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_mine = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    balance = models.CharField(max_length=250)

    

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    document1 = models.FileField(upload_to='documents/', blank=True, null=True)
    document2 = models.FileField(upload_to='documents/', blank=True, null=True)
    document3 = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return f'Profile for {self.user.username}'

