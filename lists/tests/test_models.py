# coding = utf-8

from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError
# from django.http import HttpRequest
# from django.template.loader import render_to_string
# Create your tests here.


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list_id = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        '''查看数据库是否会保存空数据'''
        list_ = List.objects.create()
        item = Item(list_id=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        '''保存相同ID,相同text是否会报错'''
        list_ = List.objects.create()
        Item.objects.create(list_id=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list_id=list_, text='bla')
            item.full_clean()
            # item.save()

    def test_CAN_save_same_item_to_different_lists(self):
        '''保存不同ID,相同text是否会报错'''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list_id=list1, text='bla')
        item = Item(list_id=list2, text='bla')
        item.full_clean()


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        '''获取显示单个模型对象的页面URL'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
