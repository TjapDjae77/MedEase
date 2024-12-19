from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'doctor', 'package_type', 'total_amount', 
                   'payment_method', 'payment_status', 'created_at')
    list_filter = ('package_type', 'payment_method', 'payment_status')
    search_fields = ('user__username', 'doctor__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informasi Pembayaran', {
            'fields': ('user', 'doctor', 'package_type')
        }),
        ('Detail Biaya', {
            'fields': ('consultation_fee', 'admin_fee', 'total_amount')
        }),
        ('Status', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
