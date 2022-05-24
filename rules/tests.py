from django.test import TestCase
from django.urls import reverse


class RulesViewTest(TestCase):

    def test_open_rules(self):
        resp = self.client.get(reverse('pokerRules'))
        self.assertEqual(resp.status_code, 200)
