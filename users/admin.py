from django.contrib import admin
from django.db.models import fields
from django.db.models import Q
from import_export.admin import ImportExportModelAdmin

from django.contrib.auth.admin import UserAdmin 

from django.contrib.gis.admin import OSMGeoAdmin
from users.resources import DentistResource


from .models import Address, Dentist, Link, Location, User, Verification

# Register your models here.

class UserAdminModel(admin.ModelAdmin):
    list_display = ('full_name', 'phone_num','role')
    list_filter = ('role','date_of_birth')
    list_per_page = 25
    

    search_fields = ('phone_num','full_name')

    def get_search_results(self, request, queryset, search_term):
        query =  User.objects.filter(Q(full_name__contains=search_term) | Q(phone_num__contains= search_term))


        _, use_distinct = super().get_search_results(request, queryset, search_term)

        return query, use_distinct

class DentistModel(ImportExportModelAdmin,admin.ModelAdmin):
    
    list_display = ('id','verified','rating','experience_year')
    list_filter = ('verified',)
    list_per_page = 25
    resource_class = DentistResource
    search_fields = ('id',)
    def get_search_results(self, request, queryset, search_term):
        query =  User.objects.filter(Q(full_name__contains=search_term) | Q(phone_num__contains= search_term)).filter(role="Dentist")


        # _, use_distinct = super().get_search_results(request, queryset, search_term)

        return query,True



class LocationAdmin(OSMGeoAdmin,admin.ModelAdmin):
    list_display = ('full_name','phone_num','location','id')
    list_per_page = 25
    search_fields = ('id',)
    def phone_num(self,obj):
        return obj.id.id.phone_num
    def full_name(self,obj):
        return obj.id.id.full_name

    def get_search_results(self, request, queryset, search_term):
        query =  User.objects.filter(Q(full_name__contains=search_term) | Q(phone_num__contains= search_term)).filter(role="Dentist")


        # _, use_distinct = super().get_search_results(request, queryset, search_term)

        return query,True



class LinkAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone_num','id')
    list_per_page = 25
    search_fields = ('id',)

    def full_name(self,obj):
        return obj.id.id.full_name
    def phone_num(self,obj):
        return obj.id.id.phone_num
    def get_search_results(self, request, queryset, search_term):
        query =  User.objects.filter(Q(full_name__contains=search_term) | Q(phone_num__contains= search_term)).filter(role="Dentist")


        # _, use_distinct = super().get_search_results(request, queryset, search_term)

        return query,True

class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone_num','id')
    list_per_page = 25
    search_fields = ('id',)

    def full_name(self,obj):
        return obj.id.id.full_name
    def phone_num(self,obj):
        return obj.id.id.phone_num
    def get_search_results(self, request, queryset, search_term):
        query =  User.objects.filter(Q(full_name__contains=search_term) | Q(phone_num__contains= search_term)).filter(role="Dentist")


        # _, use_distinct = super().get_search_results(request, queryset, search_term)

        return query,True

admin.site.register(User, UserAdminModel)
admin.site.register(Dentist,DentistModel)
admin.site.register(Verification)
admin.site.register(Location,LocationAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Link,LinkAdmin)
