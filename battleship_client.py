import sys, os, socket, select, time
from battleship_utils import send_json, receive_json
import battleship_view as view

class Client_Game(object):
	def __init__(self, opponent_no, player_no, board_space, ships_key, parent):
		self.opponent_no = opponent_no
		self.player_no = player_no
		self.board_space = board_space
		self.ships_key = ships_key
		self.parent = parent
	
	def display_battle_state(self, battle_data):
		attacker = battle_data.get('attacker')
		target = battle_data.get('target')
		attack_result = battle_data.get('attack_result')
		opponent_board = battle_data.get('opponent_board')
		player_board = battle_data.get('player_board')
		opponent_fleet_sunk = battle_data.get('opponent_fleet_sunk')
		player_fleet_sunk = battle_data.get('player_fleet_sunk')
		os.system('cls' if os.name == 'nt' else 'clear')
		if attacker == self.player_no: view.print_attack_result(attack_result, target)
		elif attacker == self.opponent_no: view.print_damage_report(attack_result, target)
		print
		view.print_board(self.board_space, opponent_board)
		view.print_board(self.board_space, player_board, self.ships_key)
		if opponent_fleet_sunk == True: view.print_success()
		elif player_fleet_sunk == True: view.print_defeat()
		if opponent_fleet_sunk == True or player_fleet_sunk == True:
			self.parent.end_game(self)
	
	def send_orders_response(self, sock):
		target_coordinates = view.get_admirals_orders()
		send_json(sock, {'orders': {'coordinates': target_coordinates}})
	
	def opponent_disconnected(self):
		print('your opponent disconnected from the server')
		self.parent.end_game(self)

class Client(object):
	def __init__(self):	
		if(len(sys.argv) < 3) :
			print('Usage : python battleship_client.py ServerIpAddress Port')
			sys.exit()

		HOST, PORT = sys.argv[1], int(sys.argv[2])
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(2)
		self.socket_list = [self.sock]
		self.current_game_session = None
		
		try: self.sock.connect((HOST, PORT))
		except: print('Unable to connect'); sys.exit()
		print('Connected to remote host.')
		
		self.send_queue_request()

	def send_queue_request(self):
		print('Entering the servers game queue')
		time.sleep(10)
		send_json(self.sock, {'queue_request': {}})
	
	def start_game(self, game_init_data):
		opponent_no = game_init_data.get('opponent_no')
		player_no = game_init_data.get('player_no')
		player_board = game_init_data.get('player_board')
		ships_key = game_init_data.get('player_ships')
		board_space = game_init_data.get('board_space')
		self.current_game_session = Client_Game(opponent_no, player_no, board_space, ships_key, self)
		
		os.system('cls' if os.name == 'nt' else 'clear')
		view.print_brief(board_space, player_board, ships_key)
		time.sleep(60)
		
	def end_game(self, game):
		self.current_game_session = None
		self.send_queue_request()

	def main(self):
		while 1:
			ready_to_read,ready_to_write,in_error = select.select(self.socket_list , [], [])
			for sock in ready_to_read:
				data = receive_json(sock)
				if data:
					if 'game_init_data' in data:
						game_init_data = data.get('game_init_data')
						self.start_game(game_init_data)
					elif 'battle_data' in data:
						battle_data = data.get('battle_data')
						self.current_game_session.display_battle_state(battle_data)
					elif 'orders_request' in data and data['orders_request'] == True:
						self.current_game_session.send_orders_response(sock)
					elif 'opponent_disconnected' in data:
						self.current_game_session.opponent_disconnected()
				else:
					print('Disconnected from server')
					sys.exit()

if __name__ == "__main__":
	Client().main()