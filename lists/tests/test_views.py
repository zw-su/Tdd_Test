# coding = utf-8

from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm
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
        self.assertIsInstance(response.context['form'], ItemForm())
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

    def test_passes_corrent_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_saving_POST_request(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'item_text': 'A new list item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item for an existing list')
        self.assertEqual(new_item.list_id, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'item_text': 'A new-old list item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
        # self.assertEqual(response.context['list'], correct_list)

    def test_validation_errors_are_sent_back_home(self):
        '''测试数据为空时，是否会显示错误'''
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/', data={'item_text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expect_error = '你不能输入一个空的待办事项'
        self.assertContains(response, expect_error)


# class NewListTest(TestCase):

#     def test_validation_errors_are_sent_back_home(self):
#         '''测试数据为空时，是否会显示错误'''
#         response = self.client.post('/lists/new', data={'item_text': ''})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home.html')
#         expect_error = '你不能输入一个空的待办事项'
#         self.assertContains(response, expect_error)

#     def test_invalid_list_items_arent_saved(self):
#         '''测试数据为空时，数据库是否会保存'''
#         self.client.post('/lists/new', data={'item_text': ''})
#         self.assertEqual(List.objects.count(), 0)
#         self.assertEqual(Item.objects.count(), 0)
