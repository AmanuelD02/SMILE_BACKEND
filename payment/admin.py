from django.contrib import admin

from payment.models import Wallet
from users.models import User
from django.db.models import Q
# Register your models here.

class WalletAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone_num','id')
    list_per_page = 25
    search_fields = ('id',)

    def full_name(self,obj):
        return obj.id.full_name
    def phone_num(self,obj):
        return obj.id.phone_num
    def get_search_results(self, request, queryset, search_term):
        query =  User.objects.filter(Q(full_name__contains=search_term) | Q(phone_num__contains= search_term))


        # _, use_distinct = super().get_search_results(request, queryset, search_term)

        return query,True


admin.site.register(Wallet,WalletAdmin)