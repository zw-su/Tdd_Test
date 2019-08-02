# coding = utf-8

from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item
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

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')
        result = response.content.decode('utf-8')
        self.assertIn('itemey 1', result)
        self.assertIn('itemey 2', result)


class ItemModelTest(TestCase):

    def test_only_save(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_saving_POST_request(self):
        response = self.client.post('/',
                                    data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
