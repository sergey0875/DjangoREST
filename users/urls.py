from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsListCreateAPIView

app_name = UsersConfig.name

urlpatterns = [

    path('payments/', PaymentsListCreateAPIView.as_view(), name='payments_list'),
]