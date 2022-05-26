from django.test import TransactionTestCase
from django.test import Client
from django.urls import reverse, reverse_lazy
from .test_utils import *
from accounts.models import CustomUser
from poker.models import Room, Players
from tables.models import Table


class IntegrationTest(TransactionTestCase):
    def setUp(self):
        self.userDB, self.tableDB, self.roomDB, self.playersDB = database()

    def test_index(self):
        c = Client()
        resp = c.get('/')
        self.assertEquals(resp.status_code, 200)
        c2 = Client()
        resp = c2.get('/asfasdf')
        self.assertEquals(resp.status_code, 404)

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
        self.assertIsNotNone(CustomUser.objects.filter(username='skorol').get())

    def test_login(self):
        c = Client()
        resp = c.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)
        resp = c.post(reverse_lazy('login'), data={
            'username': 'skorol',
            'password': 'STrongPassw0rd'
        })
        test_user = userDB.objects.get(username='skorol')
        self.assertTrue(test_user.is_authenticated)

    def test_create_table(self):
        c = Client()
        test_user = self.userDB
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
        self.assertEqual(table_count, 2)

    def test_start_game(self):
        client_1 = Client()
        client_2 = Client()
        test_user_1 = CustomUser.objects.create_user(username='sKorol', password='STrongPassw0rd')
        test_user_2 = CustomUser.objects.create_user(username='SkoRol', password='STrongPassw0rd')
        test_table = Table.objects.create(name='Table', buyIn=300, maxNoOfPlayers=3)
        client_1.force_login(test_user_1)
        client_2.force_login(test_user_2)
        resp = client_1.get('/poker/2/')
        resp = client_2.get('/poker/2/')
        room = Room.objects.all().count()
        client_1.logout()
        client_2.logout()
        self.assertEqual(room, 1)

    def test_join_game(self):
        c = Client()
        c.force_login(CustomUser.objects.create_user(username='user', password='password'))
        resp = c.get('/poker/6/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='game.html')

    def test_logout(self):
        c = Client()
        c.login(username='sKorol', password='STrongPassw0rd')
        resp = c.get('/')
        self.assertEquals(resp.status_code, 200)
        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

    def test_leave_game(self):
        c = Client()
        resp = c.get('/poker/5/')
        resp = c.post(reverse_lazy('login'), data={
            'username': 'skorol',
            'password': 'STrongPassw0rd'
        })
        self.assertEqual(resp.status_code, 200)
        resp = c.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_fold(self):
        pass

    def test_raise(self):
        pass
