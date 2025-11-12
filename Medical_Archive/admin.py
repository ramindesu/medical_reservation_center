from django.contrib import admin

# Register your models here.
from .models import Specialty, History

# Register your models here.


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("title",) 
    search_fields = ("title",) 
    ordering = ("title",) 

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ("patient", "history")
    search_fields = ("history",)   
    list_filter = ("patient",)    
    list_per_page = 50