# coding = utf-8

# 第一个TDD测试的脚本


# from unittest import skip
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from selenium.webdriver.common.by import By


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 爱吃素访问首页，不小心提交了一个空待办事项
        # 输入框中没输入内容，她就按下了回车键
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_id('id_input').send_keys(Keys.ENTER)

        # 首页刷新了，显示一个错误信息
        # 提示待办事项不能为空
        self.wait_for(lambda: self.assertEqual(self.driver.find_element_by_css_selector('.has-error'),
                                               '你不能输入一个空的待办事项'))

        # self.assertEqual(self.driver.find_element_by_css_selector('.has-error'),
        # "你不能输入一个空的待办事项")

        # 她输入一些文字，然后再次提交，这次没问题了
        self.driver.find_element_by_id('id_input').send_keys('buy milk')
        self.driver.find_element_by_id('id_input').send_keys('buy milk')
        self.check_rowtext_in_listTable('1: buy milk')

        # 她有点了调皮，又提交了一个空待办事项
        self.driver.find_element_by_id('id_input').send_keys(Keys.ENTER)

        # 在清单页面她看到了一个类似的错误信息
        self.wait_for(lambda: self.assertEqual(self.driver.find_element_by_css_selector('.has-error'),
                                               '你不能输入一个空的待办事项'))
        # 输入文字之后就没问题了
        self.driver.find_element_by_id('id_input').send_keys('buy banana')
        self.driver.find_element_by_id('id_input').send_keys('buy banana')
        self.check_rowtext_in_listTable('2: buy banana')
