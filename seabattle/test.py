from django.test import TestCase

from .services import SeaGame, Chat
from .utils import check_ship, check_around, check_posible
from .utils import check_place,  check_contact, hidden_ships


class ServicesTestCase(TestCase):
    game = SeaGame('u1', 'u2')


    def test_create_ship(self):
        self.game.build_fleet(0, 0, 4, True, 'u1')
        result = all(self.game.battlefields['u1'][0][0:2])
        self.assertTrue(result)

        self.game.build_fleet(0, 8, 4, True, 'u1')
        result = all(self.game.battlefields['u1'][0][7:9])
        self.assertTrue(not result)


    def test_check_ship(self):
        result = check_ship(3, 3, 4, True, self.game.battlefields['u1'])
        self.assertTrue(result)

        result = check_ship(0, 0, 4, True, self.game.battlefields['u1'])
        self.assertTrue(not result)

    def test_check_around(self):
        result = check_around(5, 5, self.game.battlefields['u1'])
        self.assertTrue(not result)

        self.game.build_fleet(0, 0, 4, True, 'u1')
        result = check_around(1, 1, self.game.battlefields['u1'])
        self.assertTrue(result)

    def test_check_posible(self):
        result = check_posible(5, 5, 4, True, self.game.battlefields['u1'])
        self.assertTrue(not result)

        result = check_posible(8, 8, 4, True, self.game.battlefields['u1'])
        self.assertTrue(result)

    def test_check_place(self):
        result = check_place(0, 0, self.game.battlefields['u1'])
        self.assertTrue(result)

        result = check_place(7, 7, self.game.battlefields['u1'])
        self.assertTrue(not result)

    def test_check_contact(self):
        result = check_contact(5, 5, 4, True, self.game.battlefields['u1'])
        self.assertTrue(not result)

    def test_hidden_ships(self):
        result = hidden_ships(self.game.battlefields['u1'])
        self.assertTrue(not result[0][0])
