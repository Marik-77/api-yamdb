from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, SignUpView, TokenView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router.urls)),
]
