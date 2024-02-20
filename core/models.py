from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models


# Create your models here.
class UserAccount(AbstractUser):
    username = models.CharField(
        max_length=256, validators=[MaxLengthValidator(256)], unique=True, null=False, blank=False
    )
    first_name = models.CharField(max_length=256, validators=[MaxLengthValidator(256)], null=False, blank=False)
    last_name = models.CharField(max_length=256, validators=[MaxLengthValidator(256)], null=False, blank=False)

    type_user = 'user'
    type_moderator = 'moderator'
    type_admin = 'admin'
    type_user_choice = (
        (type_user, 'user'),
        (type_moderator, 'moderator'),
        (type_admin, 'admin')
    )
    account_type = models.CharField(choices=type_user_choice, default=type_user, max_length=64)
    is_active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.username)


class Subscription(models.Model):
    subscription_link = models.TextField(
        max_length=512, validators=[MaxLengthValidator(512)], null=True, blank=True
    )
    is_active = models.BooleanField(default=False)

    creator = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, null=True, blank=True, related_name="subscriptions_creator"
    )
    assigned_to = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, null=True, blank=True, related_name="subscriptions_assignee"
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            self.creator = self.assigned_to
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.assigned_to)