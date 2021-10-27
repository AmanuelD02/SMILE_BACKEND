from django.contrib import admin
from .models import Appointment, AppointmentChat, AppointmentMessage, Availability, PendingAppointment
# Register your models here.
admin.site.register(Appointment)
admin.site.register(Availability)
admin.site.register(PendingAppointment)
admin.site.register(AppointmentChat)
admin.site.register(AppointmentMessage)