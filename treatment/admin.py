from django.contrib import admin
from .models import Treatment, TreatmentName
# Register your models here.

admin.site.register(TreatmentName)
admin.site.register(Treatment)