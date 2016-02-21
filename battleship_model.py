from random import randint

class Ship(object):
	def __init__(self, name, coordinates):
		self.name = name
		self.coordinates = coordinates
		self.damage = 0
		self.is_floating = True

class Player(object):
	def __init__(self, board_space, ships_key, player_no, conn):
		self.board_space = board_space
		self.connection = conn
		self.turn_count = 0
		self.player_no = player_no
		self.board = []
		self.ships_key = []
		self.generate_board()
		self.generate_ships(self.board, ships_key)
		
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
			if ship.is_floating == True:
				for pair in ship.coordinates:
					if len(pair) != 0:
						if pair[0] == row and \
						   pair[1] == col:
							return False
		else:
			return True

	def generate_ships(self, board, ships_key):
		for ship in ships_key:
			while True:
				ship_coordinates = []
				orientation = self.random_orientation()
				gen_row = self.random_row(board)
				gen_col = self.random_col(board)
				if orientation == 0:
					coordinate_pair = []
					col = gen_col
					for pair in range(ship[1]):
						if self.is_out_of_range(gen_row, col): break
						elif self.is_open_water(gen_row, col): col += 1
						else: break
					else:
						col = gen_col
						for pair in range(ship[1]):
							coordinate_pair = [gen_row, col]
							ship_coordinates.append(coordinate_pair)
							col += 1
						else: boat = Ship(ship[0], ship_coordinates); self.ships_key.append(boat); break
				else:
					coordinate_pair = []
					row = gen_row
					for pair in range(ship[1]):
						if self.is_out_of_range(row, gen_col): break
						elif self.is_open_water(row, gen_col): row += 1
						else: break
					else:
						row = gen_row
						for pair in range(ship[1]):
							coordinate_pair = [row, gen_col]
							ship_coordinates.append(coordinate_pair)
							row += 1
						else: boat = Ship(ship[0], ship_coordinates); self.ships_key.append(boat); break

	def is_fleet_destroyed(self):
		destroyed_ships = 0
		for ship in self.ships_key:
			if ship.is_floating == False: destroyed_ships += 1
		if destroyed_ships == len(self.ships_key):
			return True

	def identify_ship(self, row, col):
		for ship in self.ships_key:
			for pair in ship.coordinates:
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
			ship.damage += 1
			if ship.damage == len(ship.coordinates):
				ship.is_floating = False
				for pair in ship.coordinates:
					self.board[pair[0]][pair[1]] = '*'
				return ship.name
			else:
				self.board[guess_row][guess_col] = 'H'
				return 'hit'
		else:
			self.board[guess_row][guess_col] = 'X'
			return 'miss'