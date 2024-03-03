from django.contrib import admin

from core.models import UserAccount, Subscription, PanelConnection

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Subscription)
admin.site.register(PanelConnection)
