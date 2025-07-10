
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mailboxapp import views

# API Router
router = DefaultRouter()
router.register(r'sent-emails', views.SentEmailViewSet, basename='sent-email')
router.register(r'received-emails', views.ReceivedEmailViewSet, basename='received-email')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('inbox/', views.inbox, name='inbox'),
    path('send/', views.send_email, name='send_email'),
    path('webhook/', views.webhook, name='webhook'),
]