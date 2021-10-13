from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import logging

from .services import SeaGame, Chat



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info('Create loger')


''' Store '''
players = dict()
games = dict()
chats = dict()


class MainConsumer(WebsocketConsumer):
    ''' Consomer process in recive function
        Prepare data and save in store dicts'''
    def connect(self):
        self.room_name = str(self.scope['url_route']['kwargs']['room_name'])
        self.room_group_name = f'room{self.room_name}'

        if not chats.get(self.room_name):
            chats[self.room_name] = Chat()

        async_to_sync(self.channel_layer.group_add)(
                      self.room_group_name, self.channel_name)

        logger.info('New connect')
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
                      self.room_group_name, self.channel_name)

    def receive(self, text_data):

        private = False
        text_data_json = json.loads(text_data)
        data = text_data_json.get('data')

        if text_data_json.get('type') == 'game' and self.check_exist_game():
            result = games[self.room_name].action(data)
            if data['action'] == 'create_ship':
                private = True
            text_data_json['data']['result'] = result
            logger.info('Action in game')

        elif text_data_json.get('type') == 'get_history':
            text_data_json['data']['history'] = chats[self.room_name].get_history()

        elif text_data_json.get('type') == 'registration':
            private = True
            self.registration(text_data_json['data']['username'])

        elif text_data_json.get('type') == 'get_opponent_field':
            private = True
            result = games[self.room_name].get_opponent_field(data.get('username'))
            logger.info('Get opponent field')

        elif text_data_json.get('type') == 'restore':
            text_data_json['data']['result'] = games[self.room_name].restore_game_state(data.get('username'))
            logger.info('Restore game state')


        if not text_data_json['type'] == 'chat_message':
            text_data_json['type'] = 'responce'
            logger.info('Response')
        else:
            chats[self.room_name].send_message(text_data_json)
            logger.info('Message')


        if private:
            async_to_sync(self.channel_layer.send)(self.channel_name, text_data_json)
        else:
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, text_data_json)



    def chat_message(self, event):
        if not chats[self.room_name].in_chat(event['data']['username']):
            chats[self.room_name].enter(event['data']['username'])
        self.send(json.dumps(event["data"]))

    def responce(self, event):
        self.send(json.dumps(event["data"]))

    def check_exist_game(self):
        if games.get(self.room_name):
            return True
        return False

    def create_game(self):
        player1 = players[self.room_name][0]
        player2 = players[self.room_name][1]
        games[self.room_name] = SeaGame(player1, player2)

    def registration(self, player):
        if players.get(self.room_name):
            if len(players.get(self.room_name)) == 2:
                return False
            elif player == players.get(self.room_name)[0]:
                return False
            else:
                players[self.room_name].append(player)
                self.create_game()
                logger.info('Create game')

        else:
            players[self.room_name] = [player, ]

        logger.info('Registration of a new player ')
