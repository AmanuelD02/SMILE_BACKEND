from django.contrib import admin
from .models import Clinic
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.


class ClinicAdminModel(OSMGeoAdmin,admin.ModelAdmin):
    list_display = ('name','location')


admin.site.register(Clinic,ClinicAdminModel)
