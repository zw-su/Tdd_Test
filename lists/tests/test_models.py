# coding = utf-8

from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError
# from django.http import HttpRequest
# from django.template.loader import render_to_string
# Create your tests here.


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = 'the first list item'
        first_item.list_id = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'the second item'
        second_item.list_id = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'the first list item')
        self.assertEqual(first_saved_item.list_id, list_)
        self.assertEqual(second_saved_item.text, 'the second item')

    def test_cannot_save_empty_list_items(self):
        '''查看数据库是否会保存空数据'''
        list_ = List.objects.create()
        item = Item(list_id=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        '''获取显示单个模型对象的页面URL'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')