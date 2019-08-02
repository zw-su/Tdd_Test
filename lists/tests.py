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

    def test_homepage_return_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        # 只能用于通过测试客户端获取的响应
