# coding = utf-8

from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List
# from django.http import HttpRequest
# from django.template.loader import render_to_string
# Create your tests here.


class HomePageTest(TestCase):

    def test_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        # 只能用于通过测试客户端获取的响应

    # def test_save_POST_request(self):
    #     response = self.client.post(
    #         '/', data={'item_text': '新的清单项目'})
    #     print('****^^^^', response.content.decode('utf-8'))
    #     self.assertIn('新的清单项目', response.content.decode('utf-8'))
    #     self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):

    def test_use_list_template(self):
        list_ = List.objects.create()
        print('list_', list_.id)
        other_list = List.objects.create()
        print('other_list', other_list.id)
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    # def test_displays_all_items(self):
    #     list_ = List.objects.create()
    #     print('list_ &&***', list_)
    #     Item.objects.create(text='itemey 1', list_id=list_)
    #     Item.objects.create(text='itemey 2', list_id=list_)


class NewListTest(TestCase):

    def test_saving_POST_request(self):
        response = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


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
