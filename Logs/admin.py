from django.contrib import admin
from .models import Log, Transaction

@admin.register(Log)
class AdminLog(admin.ModelAdmin):
    search_fields = ('action', 'actor', 'time')
    list_filter = ('action', 'actor', 'time')
    list_display = ('id', 'info', 'action', 'actor')

@admin.register(Transaction)
class AdminLog(admin.ModelAdmin):
    search_fields = ('amount', 'status', 'patient')
    list_filter = ('amount', 'status', 'patient')
    list_display = ('id', 'amount', 'status', 'actor', 'patient', 'reservation')

