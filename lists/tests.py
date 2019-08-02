# coding = utf-8

from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
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

    def test_save_POST_request(self):
        response = self.client.post(
            '/', data={'item_text': '新的清单项目'})
        self.assertIn('新的清单项目', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, 'home.html')
