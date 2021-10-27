from django.contrib import admin

from .models import Address, Dentist, Link, Location, User, Verification
# Register your models here.

admin.site.register(User)
admin.site.register(Dentist)
admin.site.register(Location)
admin.site.register(Address)
admin.site.register(Link)
admin.site.register(Verification)
