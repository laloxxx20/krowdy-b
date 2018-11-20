# -*- coding: utf-8 -*-
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser

from .managers import UserManager
from .validators import PhoneValidator


class User(AbstractUser):

    objects = UserManager()
    username = None
    email = models.EmailField(('email address'), unique=True)
    main_id_email = models.IntegerField(blank=True, null=True)
    phone = models.CharField(
        max_length=12, unique=True, blank=True,
        null=True, validators=[PhoneValidator()])
    main_id_phone = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Email(TimeStampedModel):
    user = models.ForeignKey(
        User, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Phone(TimeStampedModel):
    user = models.ForeignKey(
        User, related_name='phones', on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=12, unique=True, blank=True,
        null=True, validators=[PhoneValidator()])

    def __str__(self):
        return self.phone
