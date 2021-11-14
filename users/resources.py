from import_export import resources
from .models import Dentist
from import_export.fields import Field



class DentistResource(resources.ModelResource):
    full_name =  Field()
    phone_num = Field()

    def dehydrate_full_name(self,dentist):
        return dentist.id.full_name
    
    def dehydrate_phone_num(self,dentist):
        return dentist.id.phone_num
    class Meta:
        model = Dentist
        export_order  = ('id','full_name','phone_num','clinic_name','degree','appointment_rate','consultation_rate','experience_year','verified','rating','consultation_availabilty')
        fields  = ('id','clinic_name','degree','appointment_rate','consultation_rate','experience_year','verified','rating','consultation_availabilty' )
    
