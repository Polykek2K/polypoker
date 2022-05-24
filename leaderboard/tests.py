from django.test import TransactionTestCase
from django.urls import reverse


class LeaderboardViewTest(TransactionTestCase):

    def test_open_leaderboard(self):
        resp = self.client.get(reverse('leaderboard'))
        self.assertEquals(resp.status_code, 200)
