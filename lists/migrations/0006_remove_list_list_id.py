# Generated by Django 2.2.3 on 2019-08-07 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_list_list_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='list_id',
        ),
    ]
