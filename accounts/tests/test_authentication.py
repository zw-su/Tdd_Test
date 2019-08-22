# cofing = utf-8

from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordLessAuthenticationBackend as pwlab
from accounts.models import Token

User = get_user_model()
EMAIL = "zouhero365@163.com"


class AuthenticateTest(TestCase):

    def test_returns_None_if_no_token(self):
        result = pwlab().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token(self):
        email = 'zouhero365@163.com'
        token = Token.objects.create(email=email)
        user = pwlab().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token(self):
        email = 'zouhero365@163.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = pwlab().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='another@qq.com')
        desired_user = User.objects.create(email=EMAIL)
        found_user = pwlab().get_user(EMAIL)
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(pwlab().get_user(EMAIL))
