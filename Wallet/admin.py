from django.contrib import admin
from .models import Wallet

# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('balance', 'transaction', 'created_at')
    search_fields = ('balance', 'transaction', 'created_at')
    ordering = ('balance',)
