from django.contrib import admin

from .models import Payment, User


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "payment_date",
        "amount",
        "payment_method",
        "course",
        "lesson",
    ]
    list_filter = ["payment_method", "payment_date"]
    search_fields = ["user__email"]
