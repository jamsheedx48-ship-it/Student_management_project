from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLES=(
        ('admin','Admin'),
        ('student','Student')
    )

    role= models.CharField(max_length=10,choices=ROLES).