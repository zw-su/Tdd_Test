# coding = 'utf-8'

from django.db import models

# Create your models here.


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list_id = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
