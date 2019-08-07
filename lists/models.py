# coding = 'utf-8'

from django.db import models

# Create your models here.


class List(models.Model):
    list_id = models.IntegerField(default=1)


class Item(models.Model):
    text = models.TextField(default='')
    list_id = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
