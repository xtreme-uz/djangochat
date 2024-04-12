from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from rest_framework import routers

from chat import views

api_router = routers.DefaultRouter()
api_router.register(r'users', views.UserViewSet)
api_router.register(r'groups', views.GroupViewSet)
api_router.register(r'chats', views.ChatViewSet)
api_router.register(r'chat-members', views.ChatMemberViewSet)
api_router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path("api/", include(api_router.urls)),
]
