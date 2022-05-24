from django.test import TestCase, TransactionTestCase
from accounts.models import CustomUser
from django.urls import reverse


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(username="Skorol")

    def test_username_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'username')

    def test_money_count(self):
        user = CustomUser.objects.get(id=1)
        money = user._meta.get_field('money').get_default()
        self.assertEquals(money, 1000)

    def test_avatar(self):
        user = CustomUser.objects.get(id=1)
        avatar = user._meta.get_field('avatar').get_default()
        self.assertEquals(avatar, "default.png")

    def test_str_username(self):
        user = CustomUser.objects.get(id=1)
        expected_str = user.username
        self.assertEquals(expected_str, str(user))


class AccountsViewTest(TransactionTestCase):
    def setUp(self):
        CustomUser.objects.create_user(username="Skorol")

    def test_open_leaderboard(self):
        resp = self.client.get('/accounts/p/Skorol/')
        self.assertEquals(resp.status_code, 200)
