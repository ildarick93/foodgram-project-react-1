from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta:
        ordering = ['date_joined']
    
    def __str__(self):
        return self.username


class Follow(models.Model):
    subscriber = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписчик')
    subscribed_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_to',
        verbose_name='На кого подписан')

