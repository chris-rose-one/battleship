from random import randint

class Player(object):
	def __init__(self, area, player_no, conn):
		self.board_space = area
		self.connection = conn
		self.turn_count = 0
		self.player_no = player_no
		self.board = []
		self.tug = {
			'name': 'tug', 'coordinates': [[],[]],
			'damage': 0, 'is_floating': True
		}
		self.destroyer = {
			'name': 'destroyer', 'coordinates': [[],[],[]],
			'damage': 0, 'is_floating': True
		}
		self.submarine = {
			'name': 'submarine', 'coordinates': [[],[],[]],
			'damage': 0, 'is_floating': True
		}
		self.battleship = {
			'name': 'battleship', 'coordinates': [[],[],[],[]],
			'damage': 0, 'is_floating': True
		}
		self.aircraft_carrier = {
			'name': 'carrier',
			'coordinates': [[],[],[],[],[]],
			'damage': 0, 'is_floating': True
		}
		self.ships_key = [self.aircraft_carrier, self.battleship, self.submarine, self.destroyer, self.tug]
		self.generate_board()
		self.generate_ships(self.board)

	def generate_board(self):
		for x in range(self.board_space):
			self.board.append(['~'] * self.board_space)

	def random_orientation(self):
		return randint(0, 1)

	def random_row(self, board):
		return randint(0, len(self.board) - 1)

	def random_col(self, board):
		return randint(0, len(self.board[0]) - 1)

	def is_out_of_range(self, row, col):
		if (row < 0 or row > (self.board_space - 1)) or \
		   (col < 0 or col > (self.board_space - 1)):
				return True

	def is_open_water(self, row, col):
		for ship in self.ships_key:
			if ship['is_floating'] == True:
				for pair in ship['coordinates']:
					if len(pair) != 0:
						if pair[0] == row and \
						   pair[1] == col:
							return False
		else:
			return True

	def generate_ships(self, board):
		for ship in self.ships_key:
			while True:
				orientation = self.random_orientation()
				gen_row = self.random_row(board)
				gen_col = self.random_col(board)
				if orientation == 0:
					col = gen_col
					for pair in ship['coordinates']:
						if self.is_out_of_range(gen_row, col): break
						elif self.is_open_water(gen_row, col): col += 1
						else: break
					else:
						col = gen_col
						for pair in ship['coordinates']:
							pair.append(gen_row)
							pair.append(col)
							col += 1
						else:
							break
				else:
					row = gen_row
					for pair in ship['coordinates']:
						if self.is_out_of_range(row, gen_col): break
						elif self.is_open_water(row, gen_col): row += 1
						else: break
					else:
						row = gen_row
						for pair in ship['coordinates']:
							pair.append(row)
							pair.append(gen_col)
							row += 1
						else: break

	def is_fleet_destroyed(self):
		destroyed_ships = 0
		for ship in self.ships_key:
			if ship['is_floating'] == False: destroyed_ships += 1
		if destroyed_ships == len(self.ships_key):
			return True

	def identify_ship(self, row, col):
		for ship in self.ships_key:
			for pair in ship['coordinates']:
				if pair[0] == row and \
				   pair[1] == col:
						return ship

	def resolve_attack(self, guess_row, guess_col):
		if self.is_out_of_range(guess_row, guess_col): return 'limits'
		if self.board[guess_row][guess_col] == 'X' or \
			 self.board[guess_row][guess_col] == 'H' or \
			 self.board[guess_row][guess_col] == '*':
				return 'guessed'
		elif self.is_open_water(guess_row, guess_col) == False:
			ship = self.identify_ship(guess_row, guess_col)
			ship['damage'] += 1
			if ship['damage'] == len(ship['coordinates']):
				ship['is_floating'] = False
				for pair in ship['coordinates']:
					self.board[pair[0]][pair[1]] = '*'
				return ship['name']
			else:
				self.board[guess_row][guess_col] = 'H'
				return 'hit'
		else:
			self.board[guess_row][guess_col] = 'X'
			return 'miss'