# coding = utf-8

# 第一个TDD测试的脚本


# from unittest import skip
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from selenium.webdriver.common.by import By


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.driver.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # 爱吃素访问首页，不小心提交了一个空待办事项
        # 输入框中没输入内容，她就按下了回车键
        self.driver.get(self.live_server_url)
        input_element = self.get_item_input_box()
        input_element.send_keys(Keys.ENTER)

        # 浏览器截获了请求
        # 清单页面不会加载

        self.wait_for(
            lambda: self.driver.find_element_by_css_selector('#id_text:invalid'))

        # self.assertEqual(self.get_error_element(),
        # "你不能输入一个空的待办事项")

        # 她输入一些文字，然后再次提交，这次没问题了
        input_element = self.get_item_input_box()
        input_element.send_keys('buy milk')
        input_element.send_keys(Keys.ENTER)
        self.check_rowtext_in_listTable('1: buy milk')

        # 她有点了调皮，又提交了一个空待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 浏览器这次也不会放行
        self.check_rowtext_in_listTable('1: buy milk')

        self.wait_for(
            lambda: self.driver.find_element_by_css_selector('#id_text:invalid'))
        # 输入文字之后就没问题了
        input_element = self.get_item_input_box()
        input_element.send_keys('buy banana')
        self.wait_for(
            lambda: self.driver.find_element_by_css_selector('#id_text:valid'))
        input_element.send_keys(Keys.ENTER)
        self.check_rowtext_in_listTable('2: buy banana')

    def test_cannot_add_duplicate_items(self):
        # 爱吃素访问首页，新建一个清单
        self.driver.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_rowtext_in_listTable('1: Buy wellies')

        # 她不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 她看到一条有帮助的错误消息
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            '你已经有这个待办事项了'))

    def test_error_messages_are_cleared(self):
        # 爱吃素新建了一个清单，但方法不当，所以出现了一个验证错误
        self.driver.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_rowtext_in_listTable('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()))

        # 为了消除错误，她开始在输入框中输入内容
        self.get_item_input_box().send_keys('a_test')

        # 看到错误消息消失了，她很高兴
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()))
