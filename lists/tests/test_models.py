# coding = utf-8

from django.test import TestCase
from lists.models import Item, List
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
