from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import main_view

urlpatterns = [
    path('room/<int:room>/', main_view)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
