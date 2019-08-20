# coding = utf-8

from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
from .base import FunctionalTest


TEST_EMAIL = "zouhero365@163.com"
SUBJECT = '你的待办事项登陆网址'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # 爱吃素访问这个很棒的待办事项网站
        # 第一次注意到导航栏有"登陆"区域
        # 看到要求输入电子邮件地址，她便输入了

        self.driver.get(self.live_server_url)
        self.driver.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.driver.find_element_by_name('email').send_keys(Keys.ENTER)

        # 出现一条消息，告诉她邮件已经发出
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.driver.find_element_by_tag_name('p').text))

        # 她查看邮件,看到一条信息
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # 邮箱中有个URL链接
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'could not find url in email body:{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 她点击了链接
        print(url)
        self.driver.get(url)

        # 她登陆了！
        self.wait_for(lambda:
                      self.driver.find_element_by_link_text('logged out'))

        navbar = self.driver.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
