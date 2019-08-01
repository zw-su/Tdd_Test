# coding = utf-8

# 第一个TDD测试的脚本

from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_can_start(self):
        # 爱吃素听说有一个很酷的在线代办事项应用
        # 她去看了这个应用的首页
        self.driver.get("http://localhost:8000/")

        # 她注意到网页的标题和头部都包含"To-Do"这个词
        # assert "To-Do" in driver.title
        self.assertIn("To-Do", self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        # 如 assertEqual 、assertTrue 和assertFalse 等。
        self.assertIn('To-Do', header_text)

        # 应用邀请她输入一个待办事项
        inputbox = self.driver.find_element_by_id("id_input")
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')
        # placeholder是html5新增的一个属性，当input或者textarea设置了该属性后，
        # 该值的内容将作为灰字提示显示在文本框中，当文本框获得焦点（或输入内容)时提示文字消失.

        # 她在文本框里输入"Buy peacock feathers"(购买孔雀羽毛).
        # 爱吃素的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys("Buy peacock feathers")

        # 她按回车键后，页面更新了
        # 待办事项表格中显示了"1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy peacock feathers'
                            for row in rows))

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了"Use peacock feathers to make a fly"
        self.fail('Finish the test')

        # 爱吃素做事很有条理

        # 页面再次更新, 她的清单中显示了这两个待办事项

        # 爱吃素想指定这个网战是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

# 她访问那个URL,发现她的待办事项列表还在

# 她很满意，去睡觉了


# driver.close()关闭当前窗口
# driver.quit()退出驱动关闭所有窗口

if __name__ == "__main__":
    # unittest.main(warnings='ignore')
    # warnings='ignore'的作用是禁止抛出ResourceWarning 异常。
    unittest.main()
