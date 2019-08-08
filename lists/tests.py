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
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items(self):
        correct_list = List.objects.create()        
        Item.objects.create(text='itemey 1', list_id=correct_list)
        Item.objects.create(text='itemey 2', list_id=correct_list)

        other_list = List.objects.create()        
        Item.objects.create(text='other itemey 1', list_id=other_list)
        Item.objects.create(text='other itemey 2', list_id=other_list)
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other itemey 1')


class NewListTest(TestCase):

    def test_saving_POST_request(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new list item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item for an existing list')
        self.assertEqual(new_item.list_id, correct_list)

    def test_redirects_after_POST(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new list item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
        # self.assertEqual(response.context['list'], correct_list)

    def test_passes_corrent_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


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
