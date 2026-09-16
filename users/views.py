
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from materials.serializers import PaymentsSerializer
from users.models import Payments, CustomUser
from  rest_framework.generics import CreateAPIView

from users.serializers import UsersSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product


class UsersCreateAPIView(CreateAPIView):
    serializer_class = UsersSerializer
    queryset = CustomUser.objects.all()
    permission_classes=(AllowAny,)


    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()




class PaymentsListCreateAPIView(generics.ListCreateAPIView):

    """Создание и просмотр нового платежа"""

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    ordering_fields = ('payment_date',)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product("Курс по Django")
        price = create_stripe_price(payment.payment_amount, product.id)
        session_id, payment_link = create_stripe_session(price.id)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

