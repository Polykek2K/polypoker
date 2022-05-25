from django.core.exceptions import ValidationError
from django.test import TransactionTestCase, Client
from django.urls import reverse
from tables.models import Table
from poker.models import Players, Room
from accounts.models import CustomUser


class TablesViewTest(TransactionTestCase):
    def test_open_tables(self):
        resp = self.client.get(reverse('index'))
        self.assertEquals(resp.status_code, 200)

    def test_index(self):
        client = Client()
        test_user = CustomUser.objects.create_user(username="skorol", password="skorol", money="900")
        client.login(username="skorol", password="skorol")
        resp = client.get(reverse('resetMoney'))
        self.assertRedirects(resp, '/')

    def test_create_table(self):
        client = Client()
        tset_user = CustomUser.objects.create_user(username="skorol", password="skorol")
        client.login(username="skorol", password="skorol")
        resp = client.get(reverse('tableCreateView'))
        self.assertEquals(resp.status_code, 200)


class TablesTest(TransactionTestCase):
    def test_get_no_of_players(self):
        test_user = CustomUser.objects.create_user(username="skorol", password="skorol")
        test_table = Table.objects.create(name="Table", buyIn=200, maxNoOfPlayers=3)
        test_room = Room.objects.create(table=test_table)
        test_players = Players.objects.create(user=test_user, room=test_room, moneyInTable=100)
        self.assertEquals(test_table.getNoOfPlayers(), 1)
        CustomUser.objects.filter().delete()
        self.assertEquals(test_table.getNoOfPlayers(), 0)
