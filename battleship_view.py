# input
def get_admirals_orders():
	target = []
	row, col = False, False
	while row == False:
		try: target.append(int(input('Target Row: '))); row = True
		except: print('\nTarget Row must be an integer')
	while col == False:
		try: target.append(int(input('Target Column: '))); col = True
		except: print('\nTarget Column must be an integer')
	return target

# output
def print_attack_result(result, target):
	print
	if result == 'tug': print('Hit! - You sank your opponents Tug Boat!')
	elif result == 'destroyer': print('Hit! - You sank your opponents Destroyer!')
	elif result == 'submarine': print('Hit! - You sank your opponents Submarine!')
	elif result == 'battleship': print('Hit! - You sank your opponents Battleship!')
	elif result == 'carrier': print('Hit! - You sank your opponents Aircraft Carrier!')
	elif result == 'hit': print('[%s,%s] Hit!' % (target[0], target[1]))
	elif result == 'miss': print('[%s,%s] Miss!' % (target[0], target[1]))
	elif result == 'guessed': print('You\'ve guessed that one already!')
	elif result == 'limits': print('That guess was out of range! You\'ve wasted a turn')
	print

def print_damage_report(result, target):
	print
	if result == 'tug': print('Your Tug Boat has been sent to the depths!')
	elif result == 'destroyer': print('Destroyer down!')
	elif result == 'submarine': print('Submarine destroyed!')
	elif result == 'battleship': print('Battleship sinking!')
	elif result == 'carrier': print('Aircraft Carrier is out of action!')
	elif result == 'hit': print('[%s,%s] Hit by opponent!' % (target[0], target[1]))
	elif result == 'miss': print('[%s,%s] Missed by opponnent!' % (target[0], target[1]))
	elif result == 'guessed': print('Your opponent made a repeat attack!')
	elif result == 'limits': print('Your opponent fired beyond the game scope!')
	print

def print_board(board, board_space):
	print('  '),
	for col in range(board_space):
		print('  ' + str(col)),
	print
	for index, row in enumerate(board):
		print('   |' + '---|' * board_space)
		print(str(index) + '  | ' + ' | '.join(row) + ' |')
	print('   |' + '---|' * board_space + '\n')

def print_success():
	print
	print('You have anihilated your opponents entire fleet')
	print

def print_defeat():
	print
	print('Your fleet has been destoyed')
	print