from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Road(models.Model):
    BROKEN = 'BR'
    WAITING = 'WT'
    PROCESS = 'PR'
    FINISHED = 'FD'

    STATUS_CHOICES = (
        (BROKEN, 'Убитая'),
        (WAITING, 'В ожидании ремонта'),
        (PROCESS, 'В процессе ремонта'),
        (FINISHED, 'Отремонтирована')
    )

    name = models.CharField(max_length=100,
                            verbose_name='Наименование объекта')
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES,
        default=FINISHED, verbose_name='Статус объекта')
    geolocation = models.URLField()
    contractor = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Подрядчик')
    warranty = models.DurationField(
        verbose_name='Гарантийный срок', null=True, blank=True)
    repair_date = models.DurationField(
        verbose_name='Дата ремонта', null=True, blank=True
    )


class Report(models.Model):
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=100)
    date = models.DateTimeField(auto_now_add=True,
                                verbose_name='Дата и время обращения')
    road = models.ForeignKey(
        Road, on_delete=models.PROTECT, verbose_name='Объект')
    photo = models.ImageField(verbose_name='Фото')
    text = models.TextField(verbose_name='Текст жалобы', max_length=5000)


class Rating(models.Model):
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=100)
    road = models.ForeignKey(
        Road, on_delete=models.PROTECT, verbose_name='Объект')
    rate = models.IntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(verbose_name='Комментарий', max_length=5000)


class Suggestion(models.Model):
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=100)
    text = models.TextField(verbose_name='Текст идеи', max_length=5000)
    photo = models.ImageField(verbose_name='Фото', null=True, blank=True)
