aplha_numero = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# output
def print_qa_attack():
	print('  ' + 'when prompted to make an attack.')
	print('  ' + 'type any combination of a row letter[A-J] and a')
	print('  ' + 'column number[0-9] with no space between them,')
	print('  ' + 'and press enter. letters are not case sensitive.')
	print('  ' + 'for example: d3 D7\n')

def print_brief(board_space, player_board, ships_key):
	print
	print('  ' + ('*' * 48))
	print((' ' * 15) + '*** 60sec BRIEFING ***')
	print('  ' + ('*' * 48) + '\n')
	print('  ' + 'Objective')
	print('  ' + '=========')
	print('  ' + 'annihilate your opponents entire fleet.\n')
	print('  ' + 'How To Attack')
	print('  ' + '=============')
	print_qa_attack()
	print('  ' + 'Fleet Positioning')
	print('  ' + '=================')
	print_board(board_space, player_board, ships_key)
	for ship in ships_key:
		string = ''
		string += '  %s: ' % ship[0]
		for pair in ship[1]: string += '[%s,%s]' % (aplha_numero[pair[0]], pair[1])
		print string

def print_attack_result(result, target):
	print
	if result == 'tug': print('  ' + '[%s,%s] Hit! - You sank your opponents Tug Boat!' % (aplha_numero[target[0]], target[1]))
	elif result == 'destroyer': print('  ' + '[%s,%s] Hit! - You sank your opponents Destroyer!' % (aplha_numero[target[0]], target[1]))
	elif result == 'submarine': print('  ' + '[%s,%s] Hit! - You sank your opponents Submarine!' % (aplha_numero[target[0]], target[1]))
	elif result == 'battleship': print('  ' + '[%s,%s] Hit! - You sank your opponents Battleship!' % (aplha_numero[target[0]], target[1]))
	elif result == 'aircraft carrier': print('  ' + '[%s,%s] Hit! - You sank your opponents Aircraft Carrier!' % (aplha_numero[target[0]], target[1]))
	elif result == 'hit': print('  ' + '[%s,%s] Hit!' % (aplha_numero[target[0]], target[1]))
	elif result == 'miss': print('  ' + '[%s,%s] Miss!' % (aplha_numero[target[0]], target[1]))
	elif result == 'guessed': print('  ' + 'You\'ve guessed that one already!')
	elif result == 'limits': print('  ' + 'That guess was out of range! You\'ve wasted a turn')

def print_damage_report(result, target):
	print
	if result == 'tug': print('  ' + '[%s,%s] Your Tug Boat has been sent to the depths!' % (aplha_numero[target[0]], target[1]))
	elif result == 'destroyer': print('  ' + '[%s,%s] Destroyer down!' % (aplha_numero[target[0]], target[1]))
	elif result == 'submarine': print('  ' + '[%s,%s] Submarine destroyed!' % (aplha_numero[target[0]], target[1]))
	elif result == 'battleship': print('  ' + '[%s,%s] Battleship sinking!' % (aplha_numero[target[0]], target[1]))
	elif result == 'aircraft carrier': print('  ' + '[%s,%s] Aircraft Carrier is out of action!' % (aplha_numero[target[0]], target[1]))
	elif result == 'hit': print('  ' + '[%s,%s] Hit by opponent!' % (aplha_numero[target[0]], target[1]))
	elif result == 'miss': print('  ' + '[%s,%s] Missed by opponnent!' % (aplha_numero[target[0]], target[1]))
	elif result == 'guessed': print('  ' + 'Your opponent made a repeat attack!')
	elif result == 'limits': print('  ' + 'Your opponent fired beyond the game scope!')

def print_board(board_space, board, ships_key=[]):
	for ship in ships_key:
		for pair in ship[1]:
			if not (board[pair[0]][pair[1]] == 'H' or board[pair[0]][pair[1]] == '*'): 
				board[pair[0]][pair[1]] = '0'
	print('    '),
	for col in range(board_space):
		print('  ' + str(col)),
	print
	for index, row in enumerate(board):
		print('     |' + '---|' * board_space)
		print('  ' + aplha_numero[index] + '  | ' + ' | '.join(row) + ' |')
	print('     |' + '---|' * board_space + '\n')

def print_success():
	print('\n  ' + 'You have anihilated your opponents entire fleet')

def print_defeat():
	print('\n  ' + 'Your fleet has been destoyed')

# input
def get_admirals_orders():
	set = False
	while set == False:
		try:
			target = raw_input('  ' + 'Enter attack coordinates: ')
			letter = target[0].upper()
			number = int(target[1])
			if not (letter.isalpha() or number.isdigit()) or len(target) > 2: raise
			if letter in aplha_numero: letter = aplha_numero.index(letter)
			else: letter = 10
			set = True
		except: print; print_qa_attack(); continue
	return [letter, number]