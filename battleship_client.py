import sys, os
import select
import time
from jsonsocket import *
from battleship_view import *

opponent_no, player_no, board_space, ships_key = 0, 0, 0, []

def new_game(sock):
	print('Re-entering the servers game queue')
	time.sleep(10)
	encode(sock, {'enter_queue': {}})

def battleship_client():
	if(len(sys.argv) < 3) :
		print 'Usage : python battleship_client.py ServerAddress port'
		sys.exit()

	host, port = sys.argv[1], int(sys.argv[2])
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(2)
	socket_list = [sock]
	
	try: sock.connect((host, port))
	except: print 'Unable to connect'; sys.exit()
	print 'Connected to remote host.'
	
	while 1:
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
		 
		for sock in ready_to_read:
			data = decode(sock)
			if data:
				if 'init_data' in data:
					opponent_no = data['init_data']['opponent_no']
					player_no = data['init_data']['player_no']
					board_space = data['init_data']['board_space']
					ships_key = data['init_data']['player_ships']
				if 'battle_data' in data:
					attacker = data['battle_data']['attacker']
					target = data['battle_data']['target']
					attack_result = data['battle_data']['attack_result']
					opponent_board = data['battle_data']['opponent_board']
					player_board = data['battle_data']['player_board']
					opponent_fleet_sunk = data['battle_data']['opponent_fleet_sunk']
					player_fleet_sunk = data['battle_data']['player_fleet_sunk']
					os.system('cls' if os.name == 'nt' else 'clear')
					if attacker == player_no: print_attack_result(attack_result, target)
					elif attacker == opponent_no: print_damage_report(attack_result, target)
					print_board(opponent_board, board_space)
					print_board(player_board, board_space)
					if opponent_fleet_sunk == True: print_success()
					elif player_fleet_sunk == True: print_defeat()
					if opponent_fleet_sunk == True or player_fleet_sunk == True:
						opponent_no, player_no, board_space, ships_key = 0, 0, 0, []
						new_game(sock)
				if 'orders_request' in data:
					if data['orders_request'] == True:
						target_coordinates = get_admirals_orders()
						encode(sock, {'orders': {'coordinates': target_coordinates}})
					elif data['orders_request'] == False: 
						for ship in ships_key: print('%s: %s' % (ship['name'], ship['coordinates']))
				if 'opp_disconnect' in data:
					print('your opponent disconnected from the server')
					opponent_no, player_no, board_space, ships_key = 0, 0, 0, []
					new_game(sock)
			else:
				print 'Disconnected from server'
				sys.exit()

if __name__ == "__main__":
	sys.exit(battleship_client())