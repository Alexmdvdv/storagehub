from django.urls import path

from oauth.views import home_view, register_view, login_view, logout_user

urlpatterns = [
    path('', home_view, name="home"),
    path('user/register/', register_view, name="register"),
    path('user/login/', login_view, name="login"),
    path('user/logout/', logout_user, name="logout")
]

