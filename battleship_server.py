import sys
import select
from jsonsocket import *
from battleship_model import *

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9009
socket_list = []
game_queue = []
live_games = []

class Online_Game(object):
	def __init__(self, sock1, sock2):
		self.board_space = 10
		self.player1 = Player(self.board_space, 1, sock1)
		self.player2 = Player(self.board_space, 2, sock2)
		self.send_init_data(self.player1, self.player2)
		self.send_init_data(self.player2, self.player1)
		self.send_battle_data(self.player1, self.player2)
		self.send_battle_data(self.player2, self.player1)
		print('Player 1 connection: (%s, %s)' % self.player1.connection.getpeername())
		print('Player 2 connection: (%s, %s)' % self.player2.connection.getpeername())

	def is_it_my_turn(self, player, opponent):
		if player.is_fleet_destroyed() == True or opponent.is_fleet_destroyed() == True: return False
		elif player is self.player1 and player.turn_count == opponent.turn_count: return True
		elif player is self.player2 and player.turn_count == opponent.turn_count - 1: return True
		else: return False
	
	def direct_attack(self, sock, coordinates):
		if sock == self.player1.connection:
			self.player1.turn_count += 1
			result = self.player2.resolve_attack(coordinates[0], coordinates[1])
			fleet_destroyed = self.player2.is_fleet_destroyed()
			self.send_battle_data(self.player1, self.player2, 1, coordinates, result, opponent_fleet_sunk=fleet_destroyed)
			self.send_battle_data(self.player2, self.player1, 1, coordinates, result, player_fleet_sunk=fleet_destroyed)
		elif sock == self.player2.connection:
			self.player2.turn_count += 1
			result = self.player1.resolve_attack(coordinates[0], coordinates[1])
			fleet_destroyed = self.player1.is_fleet_destroyed()
			self.send_battle_data(self.player2, self.player1, 2, coordinates, result, opponent_fleet_sunk=fleet_destroyed)
			self.send_battle_data(self.player1, self.player2, 2, coordinates, result, player_fleet_sunk=fleet_destroyed)
		if fleet_destroyed == True: live_games.remove(self)
	
	def send_init_data(self, player, opponent):
		encode(player.connection, {'init_data': {
			'opponent_no': opponent.player_no,
			'player_no': player.player_no,
			'board_space': self.board_space,
			'player_ships': player.ships_key
			}
		})
		
	def send_battle_data(self, player, opponent, attacker=None, target=[], result='', player_fleet_sunk=False, opponent_fleet_sunk=False):
		encode(player.connection, {'battle_data': {
			'attacker': attacker, 'target': target, 'attack_result': result,
			'opponent_board': opponent.board, 'player_board': player.board,
			'opponent_fleet_sunk': opponent_fleet_sunk, 'player_fleet_sunk': player_fleet_sunk
			},
			'orders_request': self.is_it_my_turn(player, opponent),
		})
		
	def player_disconnect(self, sock):
		if sock == self.player1.connection: encode(self.player2.connection, {'opp_disconnect': {}})
		elif sock == self.player2.connection: encode(self.player1.connection, {'opp_disconnect': {}})	

def get_game_object(sock):
	for game in live_games:
		if sock == game.player1.connection or sock == game.player2.connection: return game

def start_game():
	game = Online_Game(game_queue[0], game_queue[1])
	live_games.append(game)
	for i in range(2): game_queue.remove(game_queue[0])
						
def battleship_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)
	socket_list.append(server_socket)

	print('battleship server started at %s on port %s' % (HOST, str(PORT)))

	while 1:
		ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)

		for sock in ready_to_read:
			if sock == server_socket: 
				conn, addr = server_socket.accept()
				socket_list.append(conn)
				print "Client (%s, %s) connected" % addr
				game_queue.append(conn)
				if len(game_queue) >= 2: start_game()
			else:
				try:
					data = decode(sock)
					if data:
						if 'orders' in data:
							game = get_game_object(sock)
							if game: game.direct_attack(sock, data['orders']['coordinates'])
						if 'enter_queue' in data:
							if sock not in game_queue: game_queue.append(sock)
							if len(game_queue) >= 2: start_game()
					else:
						if sock in socket_list: socket_list.remove(sock)
						if sock in game_queue: game_queue.remove(sock)
						else: 
							game = get_game_object(sock)
							if game: game.player_disconnect(sock); live_games.remove(game)
						print "Client (%s, %s) disconnected" % sock.getpeername()
				except: continue
	
	server_socket.close()

if __name__ == "__main__":
	sys.exit(battleship_server())