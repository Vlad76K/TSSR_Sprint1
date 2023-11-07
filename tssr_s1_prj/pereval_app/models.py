from datetime import datetime
from django.db import models

""" пользователи - авторы сообщений о географических объектах """
class Authors(models.Model):
    user_fam = models.CharField('Фамилия', max_length=100, default='')   # - пользователь - фамилия
    user_name = models.CharField('Имя', max_length=100, default='')      # - пользователь - имя
    user_otc = models.CharField('Отчество', max_length=100, default='')  # - пользователь - отчество
    user_phone = models.CharField('Тел.', max_length=20, default='')     # - пользователь - номер телефона
    user_email = models.CharField('Почта', max_length=50, unique=True, default='')   # - пользователь - почта

""" справочник географических объектов """
class PerevalAreas(models.Model):
    id_parent = models.IntegerField()
    title = models.CharField('Наименование', max_length=100)  # - наименование объекта

""" статусная модель """
class StatusList(models.Model):
    """  0 - new;
         1 - pending — если модератор взял в работу;
         2 - accepted — модерация прошла успешно;
         3 - rejected — модерация прошла, информация не принята. """
    parent = models.IntegerField()
    name = models.CharField('Наименование', unique=True, max_length=50)  # - наименование объекта

"""  координаты гео-объекта """
class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Ширина')    # - ширина
    longitude = models.FloatField(verbose_name='Долгота')  # - долгота
    height = models.IntegerField('Высота')                 # - высота

""" информация о географических объектах, полученная от пользователей """
class PerevalAdded(models.Model):
    users = models.ForeignKey(Authors, on_delete=models.CASCADE, default=0)   # - пользователь
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE, default=0)  # координаты гео-объекта
    add_time = models.DateTimeField('Дата', default=datetime.strptime('2000-01-01 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'))  # - дата и время создания
    """ я бы предпочел хранить данные в этой тыблице - по одним и тем же координатам разве могут находиться два объекта ?
        зачем создавать сложности при запросе информации об объекте - дополнительные join'ы"""
    # geo_latitude = models.FloatField(verbose_name='Ширина')    # - ширина
    # geo_longitude = models.FloatField(verbose_name='Долгота')  # - долгота
    # geo_height = models.IntegerField('Высота')                 # - высота
    beauty_title = models.CharField('Вид объекта', max_length=20, default='')  # - вид объекта (например: перевал, ущелье, расщелина)
    title = models.CharField('Наименование', max_length=100, default='')       # - наименование объекта
    other_titles = models.CharField('Другие наименования', max_length=124, default='')  # - другие наименования
    connect = models.CharField('Что соединяет', max_length=100, default='')    # - что соединяет
    level_winter = models.CharField('зима', max_length=10, default='')         # - категория трудности - зимой
    level_summer = models.CharField('лето', max_length=10, default='')         # - категория трудности - летом
    level_autumn = models.CharField('осень', max_length=10, default='')        # - категория трудности - осенью
    level_spring = models.CharField('весна', max_length=10, default='')        # - категория трудности - весной
    status = models.ManyToManyField(StatusList, through='StatusObjects')    # - статус информации

""" Промежуточная таблица связей гео-объектов и статусов записе о них """
class StatusObjects(models.Model):
    so_object = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)  # - связь «один ко многим» с моделью GeoObjects;
    so_status = models.ForeignKey(StatusList, on_delete=models.CASCADE)  # - связь «один ко многим» с моделью StatusInfo;

""" фотографии гео-объекта """
class PerevalImages(models.Model):
    image_go = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    # image_data = models.ImageField(verbose_name='Картинка', upload_to='images', height_field=100, width_field=100)
    image_data = models.CharField('Картинка', max_length=1024)     # картинка
    image_title = models.CharField('Заголовок', max_length=200)  # наименование картинки
