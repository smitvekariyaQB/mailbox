from django.contrib import admin
from .models import SentEmail, ReceivedEmail

@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'from_email', 'to_email', 'sent_at', 'user')
    list_filter = ('user', 'sent_at')
    search_fields = ('subject', 'from_email', 'to_email')
    date_hierarchy = 'sent_at'
    readonly_fields = ('sent_at',)

@admin.register(ReceivedEmail)
class ReceivedEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'from_email', 'to_email', 'received_at', 'user')
    list_filter = ('user', 'received_at')
    search_fields = ('subject', 'from_email', 'to_email')
    date_hierarchy = 'received_at'
    readonly_fields = ('received_at',)