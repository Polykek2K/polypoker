from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse, reverse_lazy

from accounts.models import CustomUser
from poker.models import Room
from tables.models import Table


class IntegrationTest(TransactionTestCase):
    def test_index(self):
        c = Client()
        resp = c.get('/')
        self.assertEquals(resp.status_code, 200)

    def test_create_user(self):
        c = Client()
        resp = c.get('/accounts/signup/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='signup.html')
        resp = c.post(reverse('signup'), data={
            'username': 'skorol',
            'email': 'aa@aa.aa',
        })
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        c = Client()
        test_user = CustomUser.objects.create_user(username='skorol', password='STrongPassw0rd')
        resp = c.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)
        resp = c.post(reverse_lazy('login'), data={
            'username': 'skorol',
            'password': 'STrongPassw0rd'
        })
        self.assertRedirects(resp, '/')
        self.assertTrue(test_user.is_authenticated)

    def test_create_table(self):
        c = Client()
        test_user = CustomUser.objects.create_user(username='skorol', password='STrongPassw0rd')
        c.force_login(test_user)
        resp = c.get('/create-table/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='table-form.html')
        resp = c.post(reverse('tableCreateView'), data={
            'name': 'Table',
            'buyIn': 300,
            'maxNoOfPlayers': 4
        })
        table_count = Table.objects.all().count()
        self.assertEqual(table_count, 1)

    def test_start_game(self):
        client_1 = Client()
        client_2 = Client()
        test_user_1 = CustomUser.objects.create_user(username='skorol', password='STrongPassw0rd')
        test_user_2 = CustomUser.objects.create_user(username='Skorol', password='STrongPassw0rd')
        test_table = Table.objects.create(name='table', buyIn=300, maxNoOfPlayers=3)
        client_1.force_login(test_user_1)
        client_2.force_login(test_user_2)
        resp = client_1.get('/poker/2/')
        resp = client_2.get('/poker/2/')
        room = Room.objects.all().count()
        self.assertEqual(room, 1)
