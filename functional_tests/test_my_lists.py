# coding = utf-8

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from django.contrib.auth import get_user_model


User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # 为了设定cookie,我们要先访问网站
        # 而404页面是加载最快的(django2.2.3报错 + '/404_no_such_url/')
        self.driver.get(self.live_server_url )
        self.driver.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',))

    def test_logged_in_users_lists_are_saved_session(self):
        email = 'a@b.com'
        self.driver.get(self.live_server_url)
        self.wait_to_be_logged_out(email)
        # 爱吃素是已登陆用户
        self.create_pre_authenticated_session(email)
        self.driver.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
