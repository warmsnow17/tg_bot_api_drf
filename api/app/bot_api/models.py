from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Населённый пункт')

    def __str__(self):
        return f'{self.name}'


class Road(models.Model):
    class Status(models.TextChoices):
        BROKEN = 'BR'
        WAITING = 'WT'
        PROCESS = 'PR'
        FINISHED = 'FD'

    name = models.CharField(max_length=100,
                            verbose_name='Наименование объекта')
    city = models.ForeignKey(City, on_delete=models.PROTECT,
                             verbose_name='Населённый пункт', null=True, blank=True,
                             related_name='roads')
    status = models.CharField(max_length=512, choices=Status.choices)
    geolocation = models.URLField()
    contractor = models.CharField(max_length=500, blank=True, null=True,
                                  verbose_name='Подрядчик')
    warranty = models.CharField(max_length=50, verbose_name='Гарантийный срок',
                                null=True, blank=True)
    repair_date = models.CharField(max_length=50, verbose_name='Дата ремонта',
                                   null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Report(models.Model):
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=100)

    phone = models.CharField(verbose_name='Телефон', max_length=15, default='-')

    date = models.DateTimeField(auto_now_add=True,
                                verbose_name='Дата и время обращения')
    road = models.ForeignKey(Road, on_delete=models.PROTECT,
                             verbose_name='Объект')
    photo = models.ImageField(verbose_name='Фото')
    text = models.TextField(verbose_name='Текст жалобы', max_length=5000)


class Rating(models.Model):
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=100)
    phone = models.CharField(verbose_name='Телефон', max_length=15, default='-')

    road = models.ForeignKey(Road, on_delete=models.PROTECT,
                             verbose_name='Объект')
    rate = models.IntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(10)],
                               verbose_name='Оценка')
    comment = models.TextField(verbose_name='Комментарий', max_length=5000)


class Suggestion(models.Model):
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=100)
    phone = models.CharField(verbose_name='Телефон', max_length=15, default='-')
    text = models.TextField(verbose_name='Текст идеи', max_length=5000)
    photo = models.ImageField(verbose_name='Фото', null=True, blank=True)
