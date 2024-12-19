from django.contrib import admin
from .models import Consultation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'package_type', 'consultation_date', 
                   'consultation_time', 'status', 'ended_at')
    list_filter = ('status', 'package_type', 'consultation_date')
    search_fields = ('user__username', 'doctor__name')
    date_hierarchy = 'consultation_date'
    readonly_fields = ('created_at', 'updated_at', 'ended_at')
    inlines = [MessageInline]
    
    fieldsets = (
        ('Informasi Konsultasi', {
            'fields': ('user', 'doctor', 'package_type')
        }),
        ('Jadwal', {
            'fields': ('consultation_date', 'consultation_time')
        }),
        ('Status', {
            'fields': ('status', 'payment')
        }),
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'is_from_doctor', 'content', 'created_at')
    list_filter = ('is_from_doctor', 'created_at')
    search_fields = ('content', 'consultation__user__username', 'consultation__doctor__name')
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Pesan'
