import datetime

from django.db import models

date = str(datetime.datetime.today().strftime('%H:%M:%S - %m/%d/%Y'))


class Report(models.Model):

    id = models.AutoField(
        primary_key=True,
        verbose_name='Unique number'
    )
    city = models.CharField(
        max_length=500,
        verbose_name='City for search weather'
    )
    result = models.CharField(
        max_length=500,
        verbose_name='result of job'
    )
    date = models.CharField(
        default=date,
        max_length=100,
        verbose_name='date of request',
    )

    def __str__(self):
        return self.city
