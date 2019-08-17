# coding = utf-8

# 第一个TDD测试的脚本

from selenium import webdriver
import os
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from django.test import LiveServerTestCase


class NewVisitorTest(FunctionalTest):

    def test_can_start(self):
        # 爱吃素听说有一个很酷的在线代办事项应用
        # 她去看了这个应用的首页
        self.driver.get(self.live_server_url)
        # 报Exception happened during processing of request
        # self.driver.get('http://localhost:8000')  # 数据还是走了mysql数据库

        # 她注意到网页的标题和头部都包含"To-Do"这个词
        # assert "To-Do" in driver.title
        self.assertIn("To-Do", self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        # 如 assertEqual 、assertTrue 和assertFalse 等。
        self.assertIn('开始', header_text)

        # 应用邀请她输入一个待办事项
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         '输入你想要做的事情')
        # placeholder是html5新增的一个属性，当input或者textarea设置了该属性后，
        # 该值的内容将作为灰字提示显示在文本框中，当文本框获得焦点（或输入内容)时提示文字消失.

        # 她在文本框里输入"Buy peacock feathers"(购买孔雀羽毛).
        # 爱吃素的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys("Buy peacock feathers")

        # 她按回车键后，页面更新了
        # 待办事项表格中显示了"1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        self.check_rowtext_in_listTable('1: Buy peacock feathers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了"Use peacock feathers to make a fly"
        # 爱吃素做事很有条理
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新, 她的清单中显示了这两个待办事项
        self.check_rowtext_in_listTable('1: Buy peacock feathers')
        self.check_rowtext_in_listTable(
            '2: Use peacock feathers to make a fly')

        # 她很满意，去睡觉了

    def test_multiple_llists_at_different_url(self):
        # 爱吃素新建了一个待办事项
        self.driver.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy fruit')
        inputbox.send_keys(Keys.ENTER)
        self.check_rowtext_in_listTable('1: Buy fruit')

        # 爱吃素想指定这个网战是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL
        su_list_url = self.driver.current_url
        self.assertRegex(su_list_url, 'lists/.+?')

        # 现在一个叫做爱吃荤的新用户访问了网站

        # 我们使用一个新浏览器会话
        # 确保爱吃素的信息不会从cookie泄漏出去
        self.driver.quit()
        self.driver = webdriver.Chrome()

        # 爱吃荤访问首页，页面中看不到爱吃素的清单
        self.driver.get(self.live_server_url)
        page_text = [i.text for i in self.driver.find_elements_by_css_selector('#id_list_table tr td')]
        self.assertNotIn('1: Buy fruit', page_text)
        # self.assertNotIn('make a fly', page_text)

        # 爱吃荤输入一个新待办事项，新建一个清单
        # 他不像爱吃素那样兴趣盎然
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.check_rowtext_in_listTable('1: Buy milk')

        # 爱吃荤获得了他的唯一URL
        hun_list_url = self.driver.current_url
        self.assertRegex(hun_list_url, 'lists/.+')
        self.assertNotEqual(hun_list_url, su_list_url)

        # 这个页面还是没有爱吃素的清单
        page_text = [i.text for i in self.driver.find_elements_by_css_selector('#id_list_table tr td')]
        self.assertNotIn('1: Buy fruit', page_text)
        self.assertIn('1: Buy milk', page_text)

        # 而且页面中有一些文字解说这个
