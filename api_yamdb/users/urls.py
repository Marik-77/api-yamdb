from django.urls import path

from .views import SignUpView, TokenView, UserMeView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),  # регистрация
    path('v1/auth/token/', TokenView.as_view(), name='token'),     # получение JWT
    path('v1/users/me/', UserMeView.as_view(), name='user-me'),    # профиль текущего пользователя
]
