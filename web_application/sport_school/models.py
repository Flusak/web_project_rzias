from collections.abc import Collection, Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
import re
from datetime import datetime, timedelta, time, date
from dateutil.relativedelta import relativedelta

# Create your models here.

# Группы
class Groups(models.Model):
    class Meta:
        db_table="groups"
        verbose_name="Группы"
        verbose_name_plural="Группы"

    id_groups=models.IntegerField(primary_key=True, verbose_name="ID группы")
    type_sport=models.TextField(verbose_name="Вид спорта")
    age_group=models.SmallIntegerField(verbose_name="Минимальный возраст для группы")
    name_group=models.TextField(verbose_name="Название группы")

    def __str__(self) -> str:
        return f'{self.id_groups} {self.type_sport} {self.name_group}'


# Валидация номера телефона при помощи регулярки
def validate_phone_number(phone_number):
    reg_pattern = re.compile(r"(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$")
    if not reg_pattern.match(phone_number):
        raise ValidationError(
            gettext_lazy('%(phone_number)s is uncorrect number'),
            params={'phone_number': phone_number}
        )
    

# Валидация ID, так как использовали в модели validate_unique
def valid_pupiles_id(id_pupiles):
    for i in Pupiles.objects.values('id_pupiles'):
        if id_pupiles == i['id_pupiles']:
            raise ValidationError(
            gettext_lazy('Воспитанник с %(id_pupiles)s ID уже есть'),
            params={'id_pupiles': id_pupiles}
            )


# Воспитанники
class Pupiles(models.Model):

    class Meta:
        db_table="pupiles"
        verbose_name="Воспитанники"
        verbose_name_plural="Воспитанники"

    Genders=(
        ('W', 'Женский'),
        ('M', 'Мужской')
    )

    id_pupiles=models.IntegerField(primary_key=True, verbose_name="ID воспитанника", validators=[valid_pupiles_id])
    first_name=models.TextField(verbose_name="Фамилия")
    second_name=models.TextField(verbose_name="Имя")
    patronymic=models.TextField(verbose_name="Отчество")
    date_birth=models.DateField(verbose_name="Дата рождения")
    id_passport=models.IntegerField(verbose_name="Номер и серия паспорта", blank=True, null=True)
    gender=models.CharField(verbose_name="Пол", choices=Genders)
    phone_number=models.TextField(verbose_name="Номер телефона", validators=[validate_phone_number])
    date_entrance=models.DateField(verbose_name="Дата поступления")
    date_didmissal=models.DateField(verbose_name="Дата отчисления", blank=True, null=True)
    degree=models.TextField(verbose_name="Разряд", blank=True, null=True)
    id_groups=models.ForeignKey(Groups, on_delete=models.RESTRICT,verbose_name="Группа", blank=True, null=True)


    # Валидация возраста для группы
    def validate_unique(self, *args, **kwargs) -> None:
        if self.id_groups is not None:
            age = date.today().year - self.date_birth.year - ((date.today().month, date.today().day) < (self.date_birth.month, self.date_birth.day))
            if self.id_groups.age_group > age:
                raise ValidationError(
                            gettext_lazy('%(age)s маленький возраст для группы'),
                            params={'age': age}
                            )

    def __str__(self) -> str:
        return f'''{self.id_pupiles} {self.first_name} {self.second_name} {self.patronymic} {self.date_birth}
        {self.id_passport} {self.gender} {self.phone_number} {self.date_entrance} {self.date_didmissal}
        {self.degree} {self.id_groups}'''


# Тренеры
class Coach(models.Model):

    class Meta:
        db_table="coach"
        verbose_name="Тренеры"
        verbose_name_plural="Тренеры"

    id_trainer=models.IntegerField(primary_key=True, verbose_name="ID тренера")
    first_name=models.TextField(verbose_name="Фамилия")
    second_name=models.TextField(verbose_name="Имя")
    patronymic=models.TextField(verbose_name="Отчество")
    date_birth=models.DateField(verbose_name="Дата рождения")
    id_passport=models.IntegerField(verbose_name="Номер и серия паспорта")
    phone_number=models.TextField(verbose_name="Номер телефона")
    job=models.TextField(verbose_name="Специальность")
    degree=models.TextField(verbose_name="Разряд")
    date_entrance=models.DateField(verbose_name="Дата приема на работу")
    date_didmissal=models.DateField(verbose_name="Дата уволнения", blank=True, null=True)
    experience=models.SmallIntegerField(verbose_name="Опыт работы", blank=True, null=True)

    def __str__(self) -> str:
        return f'''{self.id_trainer} {self.first_name} {self.second_name} {self.patronymic} {self.job}'''


# Групповые тренеровки
class Groups_Training(models.Model):

    class Meta:
        db_table="groups_training"
        verbose_name="Групповые треннировки"
        verbose_name_plural="Групповые треннировки"

    id_trainer=models.ForeignKey(Coach, on_delete=models.RESTRICT, verbose_name="Тренер")
    id_group=models.ForeignKey(Groups, on_delete=models.RESTRICT, verbose_name="Группа")
    training_day=models.DateTimeField(verbose_name="Дата и время тренировки")
    type_training=models.TextField(verbose_name="Тип тренировки")


    # Валидация времени занятий
    def validate_unique(self, *args, **kwargs) -> None:
        if (self.training_day.date() <= datetime.now().date() 
            or self.training_day.time() < time(9, 59, 59) 
            or self.training_day.time() > time(20, 0, 1)):
                raise ValidationError(
                    gettext_lazy('%(training_day)s неподходящее время'),
                    params={'training_day': self.training_day.strftime('%d.%m.%Y %H:%M:%S')}
                    )
        
        trainers_days = Groups_Training.objects.filter(id_trainer=self.id_trainer).values('training_day').order_by('-training_day')
        for i in trainers_days:
            print(i['training_day'])
            if not (self.training_day > i['training_day'] + timedelta(hours=1, minutes=40)):
                print(i['training_day'] + timedelta(hours=1, minutes=40))
                raise ValidationError( 
                   gettext_lazy('%(training_day)s в это время у тренера есть занятие'),
                   params={'training_day': self.training_day.strftime('%d.%m.%Y %H:%M:%S')}
                   )
            
        grous_days = Groups_Training.objects.filter(id_group=self.id_group).values('training_day').order_by('-training_day')
        for i in grous_days:
            if not (self.training_day > i['training_day'] + timedelta(hours=1, minutes=40)):
                print (i['training_day'] + timedelta(hours=1, minutes=40))
                raise ValidationError(
                   gettext_lazy('%(training_day)s в это время у группы есть занятие'),
                   params={'training_day': self.training_day.strftime('%d.%m.%Y %H:%M:%S')}
                   )


# Индивидуальные группировки
class Individual_Training(models.Model):

    class Meta:
        db_table="individual_training"
        verbose_name="Индивидуальные треннировки"
        verbose_name_plural="Индивидуальные треннировки"

    id_trainer=models.ForeignKey(Coach, on_delete=models.RESTRICT,verbose_name="ID тренера")
    id_pupiles=models.ForeignKey(Pupiles, on_delete=models.RESTRICT, verbose_name="ID воспитанника")
    training_day=models.DateTimeField(verbose_name="Дата тренировки")
    type_training=models.TextField(verbose_name="Тип тренировки")


    # Валидация времени занятий
    def validate_unique(self, *args, **kwargs) -> None:
        if (self.training_day.date() <= datetime.now().date() 
            or self.training_day.time() < time(9, 59, 59) 
            or self.training_day.time() > time(20, 0, 1)):
                raise ValidationError(
                    gettext_lazy('%(training_day)s неподходящее время'),
                    params={'training_day': self.training_day.strftime('%d.%m.%Y %H:%M:%S')}
                    )
        
        trainers_days = Groups_Training.objects.filter(id_trainer=self.id_trainer).values('training_day').order_by('-training_day')
        for i in trainers_days:
            print(i['training_day'])
            if not (self.training_day > i['training_day'] + timedelta(hours=1, minutes=40)):
                print(i['training_day'] + timedelta(hours=1, minutes=40))
                raise ValidationError( 
                   gettext_lazy('%(training_day)s в это время у тренера есть занятие с группой'),
                   params={'training_day': self.training_day.strftime('%d.%m.%Y %H:%M:%S')}
                   )
            
        trainers_days = Individual_Training.objects.filter(id_trainer=self.id_trainer).values('training_day').order_by('-training_day')
        for i in trainers_days:
            print(i['training_day'])
            if not (self.training_day > i['training_day'] + timedelta(hours=1, minutes=40)):
                print(i['training_day'] + timedelta(hours=1, minutes=40))
                raise ValidationError( 
                   gettext_lazy('%(training_day)s в это время у тренера есть индивидуальное занятие с воспитанником'),
                   params={'training_day': self.training_day.strftime('%d.%m.%Y %H:%M:%S')}
                   )

        trainers_days = Individual_Training.objects.filter(id_pupiles=self.id_pupiles).values('training_day').order_by('-training_day')
        for i in trainers_days:
            print(i['training_day'])
            if not (self.training_day > i['training_day'] + timedelta(hours=1, minutes=40)):
                print(i['training_day'] + timedelta(hours=1, minutes=40))
                raise ValidationError( 
                   gettext_lazy('%(training_day)s в это время у тренера есть индивидуальное занятие с воспитанником'),
                   params={'training_day': self.training_day.strftime('%d.%m.%Y %H:%M:%S')}
                   )
            
        pupile = Pupiles.objects.filter(id_pupiles=self.id_pupiles.id_pupiles).values('id_groups')
        if pupile[0]['id_groups'] is not None:
            trainers_days = Groups_Training.objects.filter(id_group=pupile[0]['id_groups']).values('training_day').order_by('-training_day')
            for i in trainers_days:
                print(i['training_day'])
                if not (self.training_day > i['training_day'] + timedelta(hours=1, minutes=40)):
                    print(i['training_day'] + timedelta(hours=1, minutes=40))
                    raise ValidationError( 
                       gettext_lazy('%(training_day)s в это время у воспитанника есть занятие с группой'),
                       params={'training_day': self.training_day.strftime('%d.%m.%Y %H:%M:%S')}
                       )


    def __str__(self) -> str:
        return f'{self.id_trainer} {self.id_pupiles} {self.training_day} {self.type_training}'
