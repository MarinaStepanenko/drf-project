from itertools import product

import stripe
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from materials.models import Course
from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["payment_date"]

    def create(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"error": "Не передан course_id"}, status=status.HTTP_400_BAD_REQUEST
            )
        course = get_object_or_404(Course, id=course_id)

        amount = 1000

        try:
            product = stripe.Product.create(
                name=course.name,
                description=course.description or "Описание отсутствует",
            )

            price = stripe.Price.create(
                product=product.id,
                unit_amount=(amount * 100),
                currency="rub",
            )

            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": price.id,
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url="http://127.0.0.1:8000/api/payments/success/",
                cancel_url="http://127.0.0.1:8000/api/payments/cancel/",
            )
            payment_data = {
                "user": request.user.id,
                "course": course.id,
                "amount": amount,
                "payment_method": "stripe",
            }
            serializer = self.get_serializer(data=payment_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {"payment_url": session.url}, status=status.HTTP_201_CREATED
            )

        except stripe.error.StripeError as e:
            return Response(
                {"error": "Внутренняя ошибка"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
