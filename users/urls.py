from itertools import permutations

from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import PaymentsListCreateAPIView, UsersCreateAPIView

app_name = UsersConfig.name

urlpatterns = [

    path('register/', UsersCreateAPIView.as_view(), name='register'),
    path('payments/', PaymentsListCreateAPIView.as_view(), name='payments_list'),
    path('api/token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]