import os
from GateKeeper.settings import DEBUG

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
]

if DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
