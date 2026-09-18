from django.urls import path
from .views import register, dashboard, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", register, name="register"),
    path("dashboard/", dashboard, name="dashboard"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="students/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("profile/", profile, name="profile"),
]