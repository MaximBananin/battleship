import logging
from copy import deepcopy

from .utils import *


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info('Create loger')


class SeaGame():
    ''' Main class Battelship games.
        Control game process.
        Interface: self.action()'''
    battlefield_clear = [[0 for x in range(10)] for y in range(10)]
    fleet = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    ''' Store '''
    players = None
    battlefields = None
    fleets = None
    hits = None


    ''' State keeper 1:Build fleets, 2:Play game, 3:Finish '''
    state = None
    current_player = None


    def __init__(self, player1, player2):
        hit = sum(self.fleet)

        self.players = (player1, player2)
        self.battlefields = {player1: deepcopy(self.battlefield_clear),
                             player2: deepcopy(self.battlefield_clear)}
        self.fleets = {player1: deepcopy(self.fleet),
                       player2: deepcopy(self.fleet)}
        self.hits =  {player1: hit,
                      player2: hit}

        self.state = 1
        self.current_player = player1
        logger.info('Create new game')


    def build_fleet(self, x, y, size, direction, player):
        '''Creates a ship or returns False'''

        battlefield = self.battlefields[player]
        logger.info(f'create_ship for {player}')

        if check_ship(x, y, size, direction, battlefield):
            self.create_ship(x, y, size, direction, battlefield)
            del self.fleets[player][0]
            return self.battlefields[player]
        else:
            return False


    def fire(self, player, x, y):
        '''Fire take player and cords.
           Return new state place
           2: miss, 3: strike'''


        opponent = self.get_opponent_name(player)
        battlefield = self.battlefields[opponent]
        if check_place(x, y, battlefield):
            battlefield[y][x] = 3
            self.hits[opponent] -= 1

        else:
            battlefield[y][x] = 2
        return battlefield[y][x]


    def action(self, data):
        result = None
        action = data.get('action')
        player = data.get('username')
        x = data.get('x')
        y = data.get('y')

        if action == 'fire' and player == self.current_player and self.state == 2:
            result = self.fire(player, x, y)
            if result == 2:
                self.pass_move()

        elif action == 'create_ship' and self.state == 1:
            direction = data.get('direction')
            fleet = self.fleets.get(player)
            if fleet:
                size = fleet[0]
                result = self.build_fleet(x, y, size, direction, player)

        logger.info(f'Action: {action} in stage: {self.state}')
        logger.info(str(result))
        self.update_game_state()

        return result


    def restore_game_state(self, player):
        battlefield = self.battlefields[player]
        battlefield2 = self.get_opponent_field(player)
        return (battlefield, battlefield2)


    def create_ship(self, x, y, size, direction, battlefield):
        for i in range(size):
            battlefield[y][x] = 1
            if direction:
                x += 1
            else:
                y += 1

    def get_opponent_field(self, player):
        battlefield = self.battlefields[self.get_opponent_name(player)]
        return hidden_ships(battlefield)

    def get_opponent_name(self, player):
        return self.players[int(not self.players.index(player))]

    def pass_move(self):
        self.current_player = self.get_opponent_name(self.current_player)


    def update_game_state(self):
        '''State machine
        0:Init game, 1:Build fleets, 2:Play game, 3:Finish'''

        if self.state == 1 and not any(self.fleets.values()):
            self.state = 2
        elif self.state == 2 and min(self.hits.values()) == 0:
            self.state = 3



class Chat():
    history = []
    players = []

    def send_message(self, message):
        '''Save message '''
        self.history.append(message['data'])

    def enter(self, player):
        '''Аdds the member to the chat. '''
        self.players.append(player)

    def in_chat(self, player):
        '''Check member in the chat. '''
        return player in self.players

    def get_history(self):
        return self.history
