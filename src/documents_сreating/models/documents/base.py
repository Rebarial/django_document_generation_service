from ..base import BaseModel
from django.db import models
from django.conf import settings

class BaseDocument(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', 
                             help_text='Выбор пользователя')

    class Meta:
        abstract = True