from django.contrib import admin
from .models import Pupiles, Coach, Groups, Groups_Training, Individual_Training

# Register your models here.
class Pupiles_admin(admin.ModelAdmin):
    list_display=('id_pupiles', 'first_name', 'second_name', 'patronymic', 'date_birth',
                  'id_passport', 'gender', 'phone_number', 'date_entrance','date_didmissal',
                  'degree', 'id_groups')
    
    search_fields=('id_pupiles', 'second_name', 'id_groups', 'phone_number')
    
class Coach_admin(admin.ModelAdmin):
    list_display=('id_trainer', 'first_name', 'second_name', 'patronymic', 'job')

    search_fields=('id_trainer', 'second_name', 'job', 'phone_number')

class Groups_admin(admin.ModelAdmin):
    list_display=('id_groups', 'type_sport', 'age_group', 'name_group')

    search_fields=('id_groups', 'type_sport', 'name_group')

class Groups_Training_admin(admin.ModelAdmin):
    def my_groups(self, obj):
        return obj.id_group.name_group

    def my_coach(self, obj):
        return f'{obj.id_trainer.first_name} {obj.id_trainer.second_name}'
    
    my_groups.short_description="Группа"
    my_coach.short_description="Тренер"
    

    list_display=('my_coach', 'my_groups', 'training_day', 'type_training')

    search_fields=('id_trainer__id_trainer', 'id_trainer__first_name',
                   'id_group__id_groups', 'id_group__name_group')
    
    raw_id_fields=('id_trainer', 'id_group')

class Individual_Training_admin(admin.ModelAdmin):
    list_display=('id_trainer', 'id_pupiles', 'training_day', 'type_training')

    search_fields=['id_trainer__id_trainer', 'id_trainer__first_name',
                   'id_pupiles__id_pupiles', 'id_pupiles__first_name']
    
    raw_id_fields=['id_trainer', 'id_pupiles']


admin.site.register(Pupiles, Pupiles_admin)
admin.site.register(Coach, Coach_admin)
admin.site.register(Groups, Groups_admin)
admin.site.register(Groups_Training, Groups_Training_admin)
admin.site.register(Individual_Training, Individual_Training_admin)