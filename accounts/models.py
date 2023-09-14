from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=12)
    profile_photo = models.ImageField(max_length=100, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user_profile'

class UserOTP(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='otp', default=None)
    otp = models.IntegerField()

    def __str__(self):
        return str(self.otp)
