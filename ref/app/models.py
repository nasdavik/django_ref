from django.db import models


# создем модель юзера
class User(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    auth_code = models.IntegerField(blank=True, null=True)
    invite_code = models.CharField(max_length=6, blank=True)
    activated_invite_code = models.CharField(max_length=6, blank=True)
