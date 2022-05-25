from django.test import TestCase, TransactionTestCase
from poker.poker import Player, Cards, Poker, Game, Table, Room
from accounts.models import CustomUser


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

    def test_moneyWon_cleaning(self):
        self.assertEquals(self.test_player.moneyWon, 0)

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

    def test_comCards_length(self):
        self.assertEquals(len(self.test_cards.comCards), 5)


class PokerTest(TestCase):
    def setUp(self):
        self.players = [
            Player("skorol", 1000),
            Player("nuzhdin", 1000),
            Player("trakhtenberg", 1000)
        ]
        self.cards = Cards(self.players)
        self.poker = Poker(self.players, self.cards)

    def test_Poker_init(self):
        self.assertEquals(self.poker.players, self.players)
        self.assertEquals(self.poker.C, self.cards)
        self.assertEquals(self.poker.strengthList, ['High Card', 'Pair', 'Two Pair', \
                                                    'Three of a kind', 'Straight', 'Flush', 'Full House',
                                                    'Four of a kind', \
                                                    'Straight Flush', 'Royal Flush'])

    def test_playerWin(self):
        self.poker.playerWin = self.players[0]
        self.assertEquals(self.poker.playerWin, self.players[0])

    def test_addAceAsOne(self):
        original_hand = [
            [14, 0],
            [6, 1]
        ]

        hand = original_hand.copy()
        original_hand.append([1, 0])
        self.poker.addAceAsOne(hand)
        self.assertEquals(hand, original_hand)

    def test_sorting_1(self):
        hand1 = [
            [7, 0],
            [9, 1]
        ]

        hand2 = [
            [8, 1],
            [10, 2]
        ]

        res = self.poker.sorting(hand1, hand2)
        self.assertEquals(res, True)

    def test_sorting_2(self):
        hand1 = [
            [7, 0],
            [9, 1]
        ]

        hand2 = [
            [8, 1],
            [10, 2]
        ]

        res = self.poker.sorting(hand2, hand1)
        self.assertEquals(res, False)


class GameTest(TransactionTestCase):
    def setUp(self):
        self.players = [
            Player("skorol", 900),
            Player("nuzhdin", 1000),
            Player("trakhtenberg", 1100)
        ]

        self.players[0].hand = [
            [6, 0],
            [6, 1]
        ]

        self.players[1].hand = [
            [11, 3],
            [8, 1]
        ]

        self.players[1].hand = [
            [10, 3],
            [4, 2]
        ]

        self.user0 = CustomUser.objects.create_user(username="skorol", money=1000, avatar=None)
        self.user1 = CustomUser.objects.create_user(username="nuzhdin", money=1000, avatar=None)
        self.user2 = CustomUser.objects.create_user(username="trakhtenberg", money=1000, avatar=None)

        minimumBet = 100
        dealer = 0
        self.table = Table.objects.create(name="Table1", buyIn=10, maxNoOfPlayers=4)
        self.room = Room.objects.create(table=self.table)
        self.tableGroup = 'table_' + str(self.table.pk)
        self.game = Game(minimumBet, dealer, self.tableGroup, self.table, self.players)

    def test_Game_init(self):
        self.assertEquals(self.game.minimumBet, 100)

    def test_table_group_name(self):
        self.assertEquals(self.game.tableGroup, 'table_' + str(self.table.pk))

    def test_game_players(self):
        self.assertEquals(self.game.players, self.players)
        self.assertEquals(self.game.noOfPlayers, len(self.players))

    def test_table_settings(self):
        self.assertEquals(self.game.comCount, 4)
        self.assertEquals(self.game.pot, 0)
