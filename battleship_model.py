from random import randint

class Ship(object):
	def __init__(self, name, coordinates):
		self.name = name
		self.coordinates = coordinates
		self.damage = 0
		self.is_floating = True

class Player(object):
	def __init__(self, board_space, available_ships, player_no, conn):
		self.board_space = board_space
		self.player_no = player_no
		self.connection = conn
		self.opponent = None
		self.salvo_turns_remaining = 0
		self.total_turns = 0
		self.board = []
		self.ships_key = []
		self.generate_board()
		self.generate_ships(self.board, available_ships)
		
	def generate_board(self):
		for x in range(self.board_space):
			self.board.append(['~'] * self.board_space)

	def random_orientation(self):
		return randint(0, 1)

	def random_in_range(self):
		return randint(0, self.board_space - 1)

	def is_out_of_range(self, row, col):
		if (row < 0 or row > (self.board_space - 1)) or \
		   (col < 0 or col > (self.board_space - 1)):
				return True

	def is_open_water(self, row, col):
		for ship in self.ships_key:
			if ship.is_floating == True:
				for pair in ship.coordinates:
					if len(pair) != 0:
						if pair[0] == row and pair[1] == col: return False
		else: return True

	def is_independent(self, coordinate_list):
		buffer_list = []
		for pair in coordinate_list:
			row, col = pair[0], pair[1]
			if [row - 1, col - 1] not in (coordinate_list and buffer_list): buffer_list.append([row - 1, col - 1])
			if [row - 1, col] not in (coordinate_list and buffer_list): buffer_list.append([row - 1, col])
			if [row - 1, col + 1] not in (coordinate_list and buffer_list): buffer_list.append([row - 1, col + 1])
			if [row, col + 1] not in (coordinate_list and buffer_list): buffer_list.append([row, col + 1])
			if [row + 1, col + 1] not in (coordinate_list and buffer_list): buffer_list.append([row + 1, col + 1])
			if [row + 1, col] not in (coordinate_list and buffer_list): buffer_list.append([row + 1, col])
			if [row + 1, col - 1] not in (coordinate_list and buffer_list): buffer_list.append([row + 1, col - 1])
			if [row, col - 1] not in (coordinate_list and buffer_list): buffer_list.append([row, col - 1])
		for pair in buffer_list:
			if not self.is_open_water(pair[0], pair[1]): return False
		else: return True

	def generate_ships(self, board, available_ships):
		for ship in available_ships:
			while True:
				ship_coordinates = []
				orientation = self.random_orientation()
				row = self.random_in_range()
				col = self.random_in_range()
				for pair in range(ship[1]):
					if not self.is_out_of_range(row, col) and self.is_open_water(row, col): 
						ship_coordinates.append([row,col])
						if orientation == 0: col +=1
						else: row += 1
					else: break
				else:
					if self.is_independent(ship_coordinates): 
						boat = Ship(ship[0], ship_coordinates)
						self.ships_key.append(boat)
						break

	def serialize_ships(self):
		data = []
		for ship in self.ships_key:
			data.append([ship.name, ship.coordinates])
		return data
		
	def get_no_floating_ships(self):
		data = 0
		for ship in self.ships_key:
			if ship.is_floating == True: data += 1
		return data
	
	def is_fleet_destroyed(self):
		destroyed_ships = 0
		for ship in self.ships_key:
			if ship.is_floating == False: destroyed_ships += 1
		if destroyed_ships == len(self.ships_key): return True
		else: return False

	def identify_ship(self, row, col):
		for ship in self.ships_key:
			for pair in ship.coordinates:
				if pair[0] == row and pair[1] == col: return ship

	def resolve_attack(self, guess_row, guess_col):
		if self.is_out_of_range(guess_row, guess_col): return ['limits']
		if self.board[guess_row][guess_col] == 'X' or \
			 self.board[guess_row][guess_col] == 'H' or \
			 self.board[guess_row][guess_col] == '*':
				return ['guessed']
		elif self.is_open_water(guess_row, guess_col) == False:
			ship = self.identify_ship(guess_row, guess_col)
			ship.damage += 1
			if ship.damage == len(ship.coordinates):
				ship.is_floating = False
				for pair in ship.coordinates:
					self.board[pair[0]][pair[1]] = '*'
				return ['destroyed', ship.name]
			else:
				self.board[guess_row][guess_col] = 'H'
				return ['hit', ship.name]
		else:
			self.board[guess_row][guess_col] = 'X'
			return ['miss']