from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
import uuid
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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)


class PanelConnection(models.Model):
    connection_name = models.CharField(max_length=64, null=False, blank=False)

    panel_marzban = 'Marzban'
    panel_alireza = 'x-ui alireza0'
    panel_sanaei = '3x-ui MHSanaei'
    panel_choice = (
        (panel_marzban, 'Marzban'),
        (panel_alireza, 'x-ui alireza0'),
        (panel_sanaei, '3x-ui MHSanaei')
    )
    panel_name = models.CharField(choices=panel_choice, default=panel_marzban, max_length=32)

    ssh_ip = models.CharField(max_length=64, null=True, blank=True)
    ssh_password = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.connection_name)


class Subscription(models.Model):
    subscription_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subscription_title = models.CharField(
        max_length=512,
        validators=[MaxLengthValidator(512)], null=True, blank=False
    )
    subscription_link = models.CharField(
        max_length=512,
        validators=[MaxLengthValidator(512)], null=True, blank=False
    )
    use_count = models.IntegerField(null=False, default=0)
    expose = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    panel_connection = models.ForeignKey(
        PanelConnection, on_delete=models.CASCADE,
        null=True, blank=False, related_name="panel"
    )

    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,
        null=True, blank=False, related_name="subscriptions_creator"
    )
    assigned_to = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,
        null=True, blank=False, related_name="subscriptions_assignee"
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.created_by:
            self.created_by = self.assigned_to
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return str(f'{self.subscription_title} ({self.assigned_to})')
