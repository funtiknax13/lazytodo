from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.models import User


NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = (
        ('OP', 'Открытая'), #open
        ('CL', 'Закрытая'), #close
        ('EX', 'Срочная'), #express
        ('OV', 'Просроченная') #overdue
    )

    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='задача', )
    description = models.TextField(verbose_name='описание')
    deadline = models.DateTimeField(verbose_name='дедлайн')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='OP', verbose_name='статус')

    def __str__(self):
        return f'{self.title} - {self.deadline}'

    def get_status(self):
        now = timezone.now()
        if self.status == 'OP' or self.status == 'EX':
            if self.deadline < now:
                self.status = 'OV'
            if -1 < (self.deadline - now).days < 1:
                self.status = 'EX'
        return self.status

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
