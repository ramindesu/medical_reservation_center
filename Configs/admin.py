from django.contrib import admin
from .models import Config , Blacklist 

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['key', 'value', 'description']
    ordering = ['key']
    list_per_page = 20
    readonly_fields = ['created_at']
    
    
@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'reason', 'active','get_doctor_specialty']
    list_filter = ['active', 'doctor__specialty']
    search_fields = [
        'doctor__user__first_name', 
        'doctor__user__last_name',
        'patient__user__first_name', 
        'patient__user__last_name',
        'reason'
    ]
    list_editable = ['active']
    ordering = ['-id']
    
    def get_doctor_specialty(self, obj):
        return obj.doctor.specialty.title
  

