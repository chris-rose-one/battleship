import sys, os, socket, select, time
from battleship_utils import send_json, receive_json
import battleship_view as view

class Client(object):
	
	opponent_no, player_no, board_space, ships_key = 0, 0, 0, []
	
	def __init__(self):	
		if(len(sys.argv) < 3) :
			print('Usage : python battleship_client.py ServerIpAddress Port')
			sys.exit()

		HOST, PORT = sys.argv[1], int(sys.argv[2])
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(2)
		self.socket_list = [sock]
	
		try: sock.connect((HOST, PORT))
		except: print('Unable to connect'); sys.exit()
		print('Connected to remote host.')

	def new_game(self, sock):
		print('Re-entering the servers game queue')
		time.sleep(5)
		send_json(sock, {'queue_request': {}})

	def main(self):
		while 1:
			ready_to_read,ready_to_write,in_error = select.select(self.socket_list , [], [])
			for sock in ready_to_read:
				data = receive_json(sock)
				if data:
					if 'init_data' in data:
						init_data = data.get('init_data')
						self.opponent_no = init_data.get('opponent_no')
						self.player_no = init_data.get('player_no')
						player_board = init_data.get('player_board')
						self.ships_key = init_data.get('player_ships')
						self.board_space = init_data.get('board_space')
						os.system('cls' if os.name == 'nt' else 'clear')
						view.print_brief(self.board_space, player_board, self.ships_key); time.sleep(60)
					if 'battle_data' in data:
						battle_data = data.get('battle_data')
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
							self.opponent_no, self.player_no, self.board_space, self.ships_key = 0, 0, 0, []
							self.new_game(sock)
					if 'orders_request' in data:
						if data['orders_request'] == True:
							target_coordinates = view.get_admirals_orders()
							send_json(sock, {'orders': {'coordinates': target_coordinates}})
						elif data['orders_request'] == False: print('  ' + 'Opponents turn')
					if 'opponent_disconnected' in data:
						print('your opponent disconnected from the server')
						self.opponent_no, self.player_no, self.board_space, self.ships_key = 0, 0, 0, []
						self.new_game(sock)
				else:
					print('Disconnected from server')
					sys.exit()

if __name__ == "__main__":
	Client().main()