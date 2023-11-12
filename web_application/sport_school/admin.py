from django.contrib import admin
from .models import Pupiles, Coach, Groups, Groups_Training, Individual_Training

# Register your models here.
class Pupiles_admin(admin.ModelAdmin):
    list_display=('id_pupiles', 'first_name', 'second_name', 'patronymic', 'date_birth',
                  'id_passport', 'gender', 'phone_number', 'date_entrance','date_didmissal',
                  'degree', 'id_groups')
    
class Coach_admin(admin.ModelAdmin):
    list_display=('id_trainer', 'first_name', 'second_name', 'patronymic')

class Groups_admin(admin.ModelAdmin):
    list_display=('id_groups', 'type_sport', 'age_group', 'name_group')

class Groups_Training_admin(admin.ModelAdmin):
    list_display=('id_trainer', 'id_group', 'training_day', 'type_training')

class Individual_Training_admin(admin.ModelAdmin):
    list_display=('id_trainer', 'id_pupiles', 'training_day', 'type_training')


admin.site.register(Pupiles, Pupiles_admin)
admin.site.register(Coach, Coach_admin)
admin.site.register(Groups, Groups_admin)
admin.site.register(Groups_Training, Groups_Training_admin)
admin.site.register(Individual_Training, Individual_Training_admin)