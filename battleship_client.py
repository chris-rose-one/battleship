import sys, os, socket, select, time
from jsonsocket import encode, decode
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
		encode(sock, {'queue_request': {}})

	def main(self):
		while 1:
			ready_to_read,ready_to_write,in_error = select.select(self.socket_list , [], [])
		 	for sock in ready_to_read:
				data = decode(sock)
				if data:
					if 'init_data' in data:
						opponent_no = data['init_data']['opponent_no']
						player_no = data['init_data']['player_no']
						player_board = data['init_data']['player_board']
						ships_key = data['init_data']['player_ships']
						board_space = data['init_data']['board_space']
						os.system('cls' if os.name == 'nt' else 'clear')
						view.print_brief(board_space, player_board, ships_key); time.sleep(60)
					if 'battle_data' in data:
						attacker = data['battle_data']['attacker']
						target = data['battle_data']['target']
						attack_result = data['battle_data']['attack_result']
						opponent_board = data['battle_data']['opponent_board']
						player_board = data['battle_data']['player_board']
						opponent_fleet_sunk = data['battle_data']['opponent_fleet_sunk']
						player_fleet_sunk = data['battle_data']['player_fleet_sunk']
						os.system('cls' if os.name == 'nt' else 'clear')
						if attacker == player_no: view.print_attack_result(attack_result, target)
						elif attacker == opponent_no: view.print_damage_report(attack_result, target)
						print
						view.print_board(board_space, opponent_board)
						view.print_board(board_space, player_board, ships_key)
						if opponent_fleet_sunk == True: view.print_success()
						elif player_fleet_sunk == True: view.print_defeat()
						if opponent_fleet_sunk == True or player_fleet_sunk == True:
							opponent_no, player_no, board_space, ships_key = 0, 0, 0, []
							self.new_game(sock)
					if 'orders_request' in data:
						if data['orders_request'] == True:
							target_coordinates = view.get_admirals_orders()
							encode(sock, {'orders': {'coordinates': target_coordinates}})
					if 'opponent_disconnected' in data:
						print('your opponent disconnected from the server')
						opponent_no, player_no, board_space, ships_key = 0, 0, 0, []
						self.new_game(sock)
				else:
					print 'Disconnected from server'
					sys.exit()

if __name__ == "__main__":
	Client().main()