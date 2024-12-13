from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, gateway_message_handler

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('gateway/message/', gateway_message_handler, name='gateway-message'),
]
