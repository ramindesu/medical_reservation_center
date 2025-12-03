from django.contrib import admin
from .models import User, Doctor, Patient, CapacityIncreaseRequest
from django.contrib.auth.admin import UserAdmin
from Medical_Archive.models import Specialty
from Wallet.models import Wallet


class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'Patient Profile'
    fk_name = 'user'
    fields = ['monthly_appointment_limit', 'wallet']
    readonly_fields = ['wallet']


class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Doctor Profile'
    fk_name = 'user'
    fields = ['medical_code', 'specialty',
              'monthly_reservation_capacity', 'avatar', 'wallet']
    readonly_fields = ['medical_code', 'wallet']


class CustomUserAdmin(UserAdmin):
    inlines = [PatientInline, DoctorInline]
    list_display = ['username', 'email', 'first_name', 'last_name',
                    'phone', 'role', 'is_staff', 'is_active', 'get_user_type']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']

    def get_user_type(self, obj):
        if hasattr(obj, 'patient'):
            return 'Patient'
        elif hasattr(obj, 'doctor'):
            return 'Doctor'
        elif obj.role == User.Role.ADMIN:
            return 'Admin'
        return 'Staff'
    get_user_type.short_description = 'user type'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
# ----------------------------


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'medical_code',
                    'specialty', 'monthly_reservation_capacity', 'get_active')
    list_filter = ('specialty', 'user__active')
    search_fields = ('user__first_name', 'user__last_name',
                     'user__email', 'medical_code')
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
    list_display = ('get_first_name', 'get_last_name',
                    'get_email', 'get_phone', 'get_active')
    list_filter = ('user__active',)
    search_fields = ('user__first_name', 'user__last_name',
                     'user__email', 'user__phone')
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


admin.site.register(CapacityIncreaseRequest)

# @admin.register(Admin)
# class AdminAdmin(admin.ModelAdmin):
#     list_display = ('get_first_name', 'get_last_name', 'get_email', 'get_phone', 'get_active')
#     list_filter = ('user__active',)
#     search_fields = ('user__first_name', 'user__last_name', 'user__email', 'user__phone')
#     fieldsets = (
#         (None, {
#             'fields': ('user',)
#         }),
#     )

#     def get_first_name(self, obj):
#         return obj.user.first_name
#     get_first_name.short_description = 'First Name'

#     def get_last_name(self, obj):
#         return obj.user.last_name
#     get_last_name.short_description = 'Last Name'

#     def get_email(self, obj):
#         return obj.user.email
#     get_email.short_description = 'Email'

#     def get_phone(self, obj):
#         return obj.user.phone
#     get_phone.short_description = 'Phone'

#     def get_active(self, obj):
#         return obj.user.active
#     get_active.boolean = True
#     get_active.short_description = 'Active'

# -------------------------
