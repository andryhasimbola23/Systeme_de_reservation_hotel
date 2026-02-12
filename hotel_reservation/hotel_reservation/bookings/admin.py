from django.contrib import admin
from .models import Booking, Payment, CancellationPolicy

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room_type', 'check_in_date', 'check_out_date', 
                   'status', 'total_price')
    list_filter = ('status', 'check_in_date', 'room_type__hotel')
    search_fields = ('user__username', 'room_type__hotel__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'amount', 'payment_method', 
                   'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_method')
    readonly_fields = ('created_at',)

@admin.register(CancellationPolicy)
class CancellationPolicyAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'days_before_checkin', 'penalty_percentage')
    list_filter = ('hotel',)