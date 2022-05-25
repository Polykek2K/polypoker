from django.test import TestCase
from poker.poker import Player, Cards, Poker, Game


class PlayerTest(TestCase):
    @classmethod
    def setUp(self):
        self.test_player = Player("skorol", 1000)

    def test_player_username(self):
        self.assertEquals(self.test_player.username, "skorol")

    def test_player_money(self):
        self.assertEquals(self.test_player.money, 1000)

    def test_player_increase_money(self):
        self.test_player.increaseMoney(200)
        self.assertEquals(self.test_player.money, 1200)
        self.assertEquals(self.test_player.moneyWon, 200)

    def test_player_hand(self):
        self.assertEquals(self.test_player.hand, [])

    def test_player_hand_setter(self):
        test_hand = [
            [7, 3],
            [7, 0]
        ]
        self.test_player.hand = test_hand
        self.assertEquals(self.test_player.hand, test_hand)

    def test_player_player_In(self):
        self.assertTrue(self.test_player.playerIn)

    def test_player_hand_strength(self):
        self.assertEquals(self.test_player.handStrength, '')

    def test_call_amount_getter(self):
        self.assertEquals(self.test_player.callAmount, 0)

    def test_call_amount_setter_valid(self):
        self.test_player.callAmount = 100
        self.assertEquals(self.test_player.callAmount, 100)

    def test_call_amount_setter_exception(self):
        try:
            self.test_player.callAmount = -1
        except Exception:
            self.assertRaises(Exception, 'call amount less than 0')

    def test_putIn(self):
        self.assertEquals(self.test_player.putIn, 0)

    def test_decreasePutIn(self):
        self.test_player.decreasePutIn(10)
        self.assertEquals(self.test_player.putIn, -10)

    def test_fold(self):
        self.test_player.fold()
        self.assertEquals(self.test_player.playerIn, False)

    def test_newRound(self):
        self.test_player.newRound()
        self.assertEquals(self.test_player.playerIn, True)
        self.assertEquals(self.test_player.callAmount, 0)
        self.assertEquals(self.test_player.putIn, 0)
        self.assertEquals(self.test_player.moneyWon, 0)
        self.assertEquals(self.test_player.hand, [])
        self.assertEquals(self.test_player.handStrength, '')

    def test_call(self):
        self.test_player.call(100)
        self.assertEquals(self.test_player.money, 900)
        self.assertEquals(self.test_player.putIn, 100)
        self.assertEquals(self.test_player.callAmount, 0)

    def test_call_all_in(self):
        self.test_player.call(1500)
        self.assertEquals(self.test_player.money, 0)
        self.assertEquals(self.test_player.putIn, 1000)
        self.assertEquals(self.test_player.callAmount, 0)


class CardsTest(TestCase):
    @classmethod
    def setUp(self):
        self.test_player = Player("skorol", 1000)
        self.test_cards = Cards([self.test_player])

    def test_cards_hands(self):
        self.test_cards.makeDeck()
        self.test_cards.hands()
        self.assertIsInstance(self.test_player.hand, list)

    def test_cards_convert(self):
        self.test_player.hand = [
            [7, 3],
            [7, 0]
        ]
        hand = Cards.convert(self.test_player.hand)
        self.assertEquals(hand, '7_of_clubs 7_of_hearts ')


class PokerTest(TestCase):
    pass


class GameTest(TestCase):
    pass
