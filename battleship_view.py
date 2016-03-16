class View(object):
	aplha_numero = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
	
	def __init__(self, py_version_info):
		self.py_version_major = py_version_info.major

	# output
	def print_qa_attack(self):
		print('  ' + 'when prompted to make an attack.')
		print('  ' + 'type any combination of a row letter[A-J] and a')
		print('  ' + 'column number[0-9] with no space between them,')
		print('  ' + 'and press enter. letters are not case sensitive.')
		print('  ' + 'for example: d3 D7\n')

	def print_brief(self, board_space, player_board, ships_key):
		print()
		print('  ' + ('*' * 48))
		print((' ' * 15) + '*** 60sec BRIEFING ***')
		print('  ' + ('*' * 48) + '\n')
		print('  ' + 'Objective')
		print('  ' + '=========')
		print('  ' + 'annihilate your opponents entire fleet.\n')
		print('  ' + 'How To Attack')
		print('  ' + '=============')
		self.print_qa_attack()
		print('  ' + 'Fleet Positioning')
		print('  ' + '=================')
		self.print_board(board_space, player_board, ships_key)
		for ship in ships_key:
			string = ''
			string += '  %s: ' % ship[0]
			for pair in ship[1]: string += '[%s,%s]' % (self.aplha_numero[pair[0]], pair[1])
			print(string)

	def print_attack_result(self, result, target):
		print()
		if result == 'tug': print('  ' + '[%s,%s] Hit! - You sank your opponents Tug Boat!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'destroyer': print('  ' + '[%s,%s] Hit! - You sank your opponents Destroyer!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'submarine': print('  ' + '[%s,%s] Hit! - You sank your opponents Submarine!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'battleship': print('  ' + '[%s,%s] Hit! - You sank your opponents Battleship!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'aircraft carrier': print('  ' + '[%s,%s] Hit! - You sank your opponents Aircraft Carrier!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'hit': print('  ' + '[%s,%s] Hit!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'miss': print('  ' + '[%s,%s] Miss!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'guessed': print('  ' + 'You\'ve guessed that one already!')
		elif result == 'limits': print('  ' + 'That guess was out of range! You\'ve wasted a turn')

	def print_damage_report(self, result, target):
		print()
		if result == 'tug': print('  ' + '[%s,%s] Your Tug Boat has been sent to the depths!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'destroyer': print('  ' + '[%s,%s] Destroyer down!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'submarine': print('  ' + '[%s,%s] Submarine destroyed!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'battleship': print('  ' + '[%s,%s] Battleship sinking!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'aircraft carrier': print('  ' + '[%s,%s] Aircraft Carrier is out of action!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'hit': print('  ' + '[%s,%s] Hit by opponent!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'miss': print('  ' + '[%s,%s] Missed by opponnent!' % (self.aplha_numero[target[0]], target[1]))
		elif result == 'guessed': print('  ' + 'Your opponent made a repeat attack!')
		elif result == 'limits': print('  ' + 'Your opponent fired beyond the game scope!')

	def print_board(self, board_space, board, ships_key=[]):
		for ship in ships_key:
			for pair in ship[1]:
				if not (board[pair[0]][pair[1]] == 'H' or board[pair[0]][pair[1]] == '*'): 
					board[pair[0]][pair[1]] = '0'
		if self.py_version_major == 2: print('    '),
		if self.py_version_major == 3: print('    ', end='')
		for col in range(board_space):
			if self.py_version_major == 2: print('  ' + str(col)),
			if self.py_version_major == 3: print('   ' + str(col), end='')
		print()
		for index, row in enumerate(board):
			print('     |' + '---|' * board_space)
			print('  ' + self.aplha_numero[index] + '  | ' + ' | '.join(row) + ' |')
		print('     |' + '---|' * board_space + '\n')

	def print_success(self):
		print('\n  ' + 'You have anihilated your opponents entire fleet\n')

	def print_defeat(self):
		print('\n  ' + 'Your fleet has been destoyed\n')

	# input
	def get_admirals_orders(self):
		set = False
		while set == False:
			try:
				if self.py_version_major == 2: target = raw_input('  ' + 'Enter attack coordinates: ')
				if self.py_version_major == 3: target = input('  ' + 'Enter attack coordinates: ')
				letter = target[0].upper()
				number = int(target[1])
				if not (letter.isalpha() or number.isdigit()) or len(target) > 2: raise
				if letter in self.aplha_numero: letter = self.aplha_numero.index(letter)
				else: letter = 10
				set = True
			except: print(); self.print_qa_attack(); continue
		return [letter, number]