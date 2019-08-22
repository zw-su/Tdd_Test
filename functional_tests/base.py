# coding = utf-8

# 第一个TDD测试的脚本

from selenium import webdriver
import os, time
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 8


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()

    def get_item_input_box(self):
        '''定位input元素'''
        return self.driver.find_element_by_id('id_text')

    def wait_for(self, fn):
        '''等待元素找到'''
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_to_be_logged_in(self, email):
        self.wait_for(
            lambda: self.driver.find_element_by_link_text('Log out'))
        navbar = self.driver.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for(lambda: self.driver.find_element_by_name('email'))
        navbar = self.driver.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def check_rowtext_in_listTable(self, row_text):
        # table = self.driver.find_element_by_id('id_list_table')
        locator = (By.ID, 'id_list_table')
        table = WebDriverWait(self.driver, 10).\
            until(EC.presence_of_element_located(locator))
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


if __name__ == "__main__":
    # unittest.main(warnings='ignore')
    # warnings='ignore'的作用是禁止抛出ResourceWarning 异常。
    unittest.main()
