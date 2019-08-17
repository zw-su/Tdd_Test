# coding = utf-8

import unittest
import os
from .base import FunctionalTest
from selenium.webdriver.common.by import By


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_styling(self):
        # 把浏览器窗口设置为1024*768大小
        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1024, 768)

        # 她看到了输入框完美的居中显示(测试CSS样式)
        inputbox = self.driver.find_element_by_id('id_input')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)


if __name__ == "__main__":
    # unittest.main(warnings='ignore')
    # warnings='ignore'的作用是禁止抛出ResourceWarning 异常。
    unittest.main()
