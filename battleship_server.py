import sys, os, socket, select
from battleship_utils import send_json, receive_json
import battleship_model as model

class Online_Game(object):
	def __init__(self, sock1, sock2, board_space, available_ships):
		self.board_space = board_space
		self.player1 = model.Player(board_space, available_ships, 1, sock1)
		self.player2 = model.Player(board_space, available_ships, 2, sock2)
		self.player1.opponent = self.player2
		self.player2.opponent = self.player1
		self.player_list = [self.player1, self.player2]
		self.send_init_data()
		self.send_battle_data()
		self.send_orders_request()
	
	def send_init_data(self):
		for player in self.player_list:
			send_json(player.connection, {'init_data': {
				'opponent_no': player.opponent.player_no, 'player_no': player.player_no,
				'player_board': player.board, 'player_ships': player.serialize_ships(),
				'board_space': self.board_space}
			})
		
	def send_battle_data(self, attacker=None, target=[], result=[]):
		for player in self.player_list:
			send_json(player.connection, {'battle_data': {
				'attacker': attacker, 'target': target, 'attack_result': result,
				'opponent_board': player.opponent.board, 'player_board': player.board,
				'opponent_fleet_sunk': player.opponent.is_fleet_destroyed(), 'player_fleet_sunk': player.is_fleet_destroyed()}
			})	
	
	def send_orders_request(self):
		player = self.player_list.pop(0); self.player_list.append(player)
		send_json(player.connection, {'orders_request': True})
	
	def player_disconnected(self, sock):
		player = self.get_player_by_socket(sock)
		send_json(player.opponent.connection, {'opponent_disconnected': {}})
		Server.live_games.remove(self)
	
	def get_player_by_socket(self, sock):
		for player in self.player_list:
			if player.connection == sock: return player
	
	def direct_attack(self, sock, target_coordinates):
		player = self.get_player_by_socket(sock)
		player.turn_count += 1
		attack_result = player.opponent.resolve_attack(target_coordinates[0], target_coordinates[1])
		self.send_battle_data(player.player_no, target_coordinates, attack_result)
		if player.is_fleet_destroyed == True: Server.live_games.remove(self)
		else: self.send_orders_request()

class Server(object):
	HOST = socket.gethostbyname(socket.gethostname())
	PORT = 16000
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

	def get_game(self, sock):
		for game in self.live_games:
			for player in game.player_list:
				if player.connection == sock: return game
			else: return False

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
						data = receive_json(sock)
						if data:
							if 'orders' in data:
								orders = data.get('orders').get('coordinates')
								game = self.get_game(sock)
								if game: game.direct_attack(sock, orders)
							if 'queue_request' in data:
								if sock not in self.game_queue: self.game_queue.append(sock)
								if len(self.game_queue) >= 2: self.start_game()
						else:
							if sock in self.game_queue: self.game_queue.remove(sock)
							elif self.get_game(sock): game.player_disconnected(sock)
							if sock in self.socket_list: self.socket_list.remove(sock)
							print('Client (%s, %s) disconnected' % sock.getpeername())
					except: continue
		server_socket.close()

if __name__ == "__main__":
	board_space = 10
	available_ships = [('Aircraft Carrier', 5), ('Battleship', 4), ('Destroyer', 3), ('Submarine', 3), ('Patrol Boat', 2)] 
	Server(board_space, available_ships).main()