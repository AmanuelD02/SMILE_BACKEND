from django.contrib import admin
from .models import Appointment, AppointmentChat, AppointmentMessage
# Register your models here.
admin.site.register(Appointment)
admin.site.register(AppointmentChat)
admin.site.register(AppointmentMessage)
