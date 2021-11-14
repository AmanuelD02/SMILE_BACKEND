from django.contrib import admin
from .models import Clinic
# Register your models here.

class ClinicAdminModel(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Clinic,ClinicAdminModel)
