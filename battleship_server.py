import sys, os, socket, select
from jsonsocket import encode, decode
import battleship_model as model

class Online_Game(object):
	def __init__(self, sock1, sock2, board_space, available_ships):
		self.board_space = board_space
		self.player1 = model.Player(board_space, available_ships, 1, sock1)
		self.player2 = model.Player(board_space, available_ships, 2, sock2)
		self.send_init_data(self.player1, self.player2)
		self.send_init_data(self.player2, self.player1)
		self.send_battle_data(self.player1, self.player2)
		self.send_battle_data(self.player2, self.player1)

	def is_it_my_turn(self, player, opponent):
		if player.is_fleet_destroyed() == True or opponent.is_fleet_destroyed() == True: return None
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
			'opponent_no': opponent.player_no, 'player_no': player.player_no,
			'player_board': player.board, 'player_ships': player.serialize_ships(),
			'board_space': self.board_space
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
		
	def player_disconnected(self, sock):
		if sock == self.player1.connection: encode(self.player2.connection, {'opponent_disconnected': {}})
		elif sock == self.player2.connection: encode(self.player1.connection, {'opponent_disconnected': {}})	

class Server(object):
	
	HOST = socket.gethostbyname(socket.gethostname())
	PORT = 9009
	socket_list = []
	game_queue = []
	live_games = []
	
	def __init__(self, board_space, available_ships):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((self.HOST, self.PORT))
		self.server_socket.listen(10)
		self.socket_list.append(self.server_socket)
		self.board_space = board_space
		self.available_ships = available_ships
		print('battleship server started at %s on port %s' % (self.HOST, str(self.PORT)))

	def start_game(self):
		game = Online_Game(self.game_queue[0], self.game_queue[1], self.board_space, self.available_ships)
		self.live_games.append(game)
		for i in range(2): self.game_queue.remove(self.game_queue[0])

	def get_game_object(self, sock):
		for game in self.live_games:
			if sock == game.player1.connection or sock == game.player2.connection: return game

	def main(self):
		while 1:
			ready_to_read,ready_to_write,in_error = select.select(self.socket_list,[],[],0)

			for sock in ready_to_read:
				if sock == self.server_socket: 
					conn, addr = self.server_socket.accept()
					self.socket_list.append(conn)
					print('Client (%s, %s) connected' % addr)
					self.game_queue.append(conn)
					if len(self.game_queue) >= 2: self.start_game()
				else:
					try:
						data = decode(sock)
						if data:
							if 'orders' in data:
								game = self.get_game_object(sock)
								if game: game.direct_attack(sock, data['orders']['coordinates'])
							if 'queue_request' in data:
								if sock not in self.game_queue: self.game_queue.append(sock)
								if len(self.game_queue) >= 2: self.start_game()
						else:
							if sock in self.socket_list: self.socket_list.remove(sock)
							if sock in self.game_queue: self.game_queue.remove(sock)
							else: 
								game = self.get_game_object(sock)
								if game: game.player_disconnected(sock); self.live_games.remove(game)
							print('Client (%s, %s) disconnected' % sock.getpeername())
					except: continue
		server_socket.close()

if __name__ == "__main__":
	board_space = 10
	available_ships = [('aircraft carrier', 5), ('battleship', 4), ('destroyer', 3), ('submarine', 3), ('tug', 2)]
	Server(board_space, available_ships).main()