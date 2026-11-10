from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import PaymentViewSet

router = SimpleRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("materials.urls", namespace="materials")),
    path("api/", include(router.urls)),
]
