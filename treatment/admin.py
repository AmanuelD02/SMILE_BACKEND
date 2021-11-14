from django.contrib import admin

from django.db.models.query_utils import Q

from .models import Treatment, TreatmentName
# Register your models here.
from users.models import User
class TreatmentNameAdminModel(admin.ModelAdmin):
    list_display = ('name',)
class TreatmentAdminModel(admin.ModelAdmin):
    
    list_display = ('dentist_id','name','price')
    
    list_per_page = 25


admin.site.register(TreatmentName,TreatmentNameAdminModel)
admin.site.register(Treatment,TreatmentAdminModel)