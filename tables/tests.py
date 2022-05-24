from django.test import TransactionTestCase
from django.urls import reverse
from tables.models import Table


class TablesViewTest(TransactionTestCase):
    def test_open_tables(self):
        resp = self.client.get(reverse('index'))
        self.assertEquals(resp.status_code, 200)
