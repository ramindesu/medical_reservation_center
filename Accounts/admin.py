from django.contrib import admin
from .models import Doctor, Patient, Admin


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'medical_code', 'specialty', 'monthly_reservation_capacity', 'get_active')
    list_filter = ('specialty', 'user__active')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'medical_code')
    fieldsets = (
        (None, {
            'fields': ('user', 'medical_code', 'specialty', 'monthly_reservation_capacity')
        }),
    )

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_active(self, obj):
        return obj.user.active
    get_active.boolean = True
    get_active.short_description = 'Active'



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'get_phone', 'get_active')
    list_filter = ('user__active',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'user__phone')
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
    )

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'

    def get_active(self, obj):
        return obj.user.active
    get_active.boolean = True
    get_active.short_description = 'Active'



@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'get_phone', 'get_active')
    list_filter = ('user__active',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'user__phone')
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
    )

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'

    def get_active(self, obj):
        return obj.user.active
    get_active.boolean = True
    get_active.short_description = 'Active'
