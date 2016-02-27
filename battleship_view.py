aplha_numero = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# input
def get_admirals_orders():
	set = False
	while set == False:
		try:
			target = raw_input('Enter attack coordinates: ')
			letter = target[0].upper()
			number = int(target[1])
			if not (letter.isalpha() or number.isdigit()) or len(target) > 2: raise
			if letter in aplha_numero: letter = aplha_numero.index(letter)
			else: letter = 10
			set = True
		except: continue
	return [letter, number]

# output
def print_attack_result(result, target):
	print
	if result == 'tug': print('[%s,%s] Hit! - You sank your opponents Tug Boat!' % (aplha_numero[target[0]], target[1]))
	elif result == 'destroyer': print('[%s,%s] Hit! - You sank your opponents Destroyer!' % (aplha_numero[target[0]], target[1]))
	elif result == 'submarine': print('[%s,%s] Hit! - You sank your opponents Submarine!' % (aplha_numero[target[0]], target[1]))
	elif result == 'battleship': print('[%s,%s] Hit! - You sank your opponents Battleship!' % (aplha_numero[target[0]], target[1]))
	elif result == 'aircraft carrier': print('[%s,%s] Hit! - You sank your opponents Aircraft Carrier!' % (aplha_numero[target[0]], target[1]))
	elif result == 'hit': print('[%s,%s] Hit!' % (aplha_numero[target[0]], target[1]))
	elif result == 'miss': print('[%s,%s] Miss!' % (aplha_numero[target[0]], target[1]))
	elif result == 'guessed': print('You\'ve guessed that one already!')
	elif result == 'limits': print('That guess was out of range! You\'ve wasted a turn')
	print

def print_damage_report(result, target):
	print
	if result == 'tug': print('[%s,%s] Your Tug Boat has been sent to the depths!' % (aplha_numero[target[0]], target[1]))
	elif result == 'destroyer': print('[%s,%s] Destroyer down!' % (aplha_numero[target[0]], target[1]))
	elif result == 'submarine': print('[%s,%s] Submarine destroyed!' % (aplha_numero[target[0]], target[1]))
	elif result == 'battleship': print('[%s,%s] Battleship sinking!' % (aplha_numero[target[0]], target[1]))
	elif result == 'aircraft carrier': print('[%s,%s] Aircraft Carrier is out of action!' % (aplha_numero[target[0]], target[1]))
	elif result == 'hit': print('[%s,%s] Hit by opponent!' % (aplha_numero[target[0]], target[1]))
	elif result == 'miss': print('[%s,%s] Missed by opponnent!' % (aplha_numero[target[0]], target[1]))
	elif result == 'guessed': print('Your opponent made a repeat attack!')
	elif result == 'limits': print('Your opponent fired beyond the game scope!')
	print

def print_board(board_space, board, ships_key=[]):
	for ship in ships_key:
		for pair in ship[1]:
			if not (board[pair[0]][pair[1]] == 'H' or board[pair[0]][pair[1]] == '*'): 
				board[pair[0]][pair[1]] = '0'
	print
	print('    '),
	for col in range(board_space):
		print('  ' + str(col)),
	print
	for index, row in enumerate(board):
		print('     |' + '---|' * board_space)
		print('  ' + aplha_numero[index] + '  | ' + ' | '.join(row) + ' |')
	print('     |' + '---|' * board_space + '\n')

def print_success():
	print
	print('You have anihilated your opponents entire fleet')
	print

def print_defeat():
	print
	print('Your fleet has been destoyed')
	print