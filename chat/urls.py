from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from rest_framework import routers

from chat import views

api_router = routers.DefaultRouter()
api_router.register(r'users', views.UserViewSet)
api_router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path("", views.chat_page, name="chat-page"),

    # login-section
    path("auth/login/", LoginView.as_view(template_name="chat/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path("api/", include(api_router.urls)),
]
