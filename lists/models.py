# coding = 'utf-8'

from django.db import models
from django.urls import reverse

# Create your models here.


class List(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='', blank=False)
    list_id = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        indexes = [models.Index(
            fields=['list_id'], name='item_list_id_index'), ]
        unique_together = ('list_id', 'text')
