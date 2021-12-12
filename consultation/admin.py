from django.contrib import admin
from .models import Consultation, ConsultationMessage, ConsultationRequest, PendingConsultation
# Register your models here.


admin.site.register(Consultation)
admin.site.register(PendingConsultation)
admin.site.register(ConsultationMessage)