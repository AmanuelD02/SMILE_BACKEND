from django.contrib import admin
from .models import Consultation, ConsultationMessage, ConsultationRequest
# Register your models here.


admin.site.register(Consultation)
admin.site.register(ConsultationRequest)
admin.site.register(ConsultationMessage)