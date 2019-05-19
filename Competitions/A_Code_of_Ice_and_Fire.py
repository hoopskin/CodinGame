import sys
import math

# MAP SIZE
WIDTH = 12
HEIGHT = 12

# OWNER
ME = 0
OPPONENT = 1

# BUILDING TYPE
HQ = 0

# CELL TYPE
VOID = '#'
NEUTRAL = '.'
CAPTURED_ME = 'O'
CAPTURED_OPP = 'X'
INACTIVE_ME = 'o'
INACTIVE_OPP = 'x'

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Unit:
	def __init__(self, owner, id, level, x, y):
		self.owner = owner
		self.id = id
		self.level = level
		self.upkeep = {1:1, 2:4, 3:20}[level]
		self.pos = Position(x, y)

class Building:
	def __init__(self, owner, type, x, y):
		self.owner = owner
		self.type = type
		self.pos = Position(x, y)

class Game:
	def __init__(self):
		self.board = []
		self.buildings = []
		self.units = []
		self.actions = []
		self.gold = 0
		self.income = 0
		self.opponent_gold = 0
		self.opponent_income = 0
		self.message = "MSG hello"

	def get_my_HQ(self):
		for b in self.buildings:
			if b.type == HQ and b.owner == ME:
				return b

	def get_opponent_HQ(self):
		for b in self.buildings:
			if b.type == HQ and b.owner == OPPONENT:
				return b

	def move_units(self):
		#Kill ability: 1=NA, 2=1, 3=All
		#Ergo, 1 = Gathers, 2=Jaime, 3=Arya

		#Zombie Wakanda plan. Just keep going at them.
		loc = self.get_opponent_HQ().pos

		for unit in self.units:
			if unit.owner == ME:
				self.actions.append(f'MOVE {unit.id} {loc.x} {loc.y}')

	def get_train_position(self):
		# TODO: this just puts a unit at the HQ. Safe, but fix
		hq = self.get_my_HQ()

		if hq.pos.x == 0:
			return Position(0, 1)
		return Position(11, 10)


	def train_units(self):
		train_pos = self.get_train_position()

		#Recruit Costs: 1=10, 2=20, 3=30
		#Kill ability: 1=NA, 2=1, 3=All
		#Ergo, 1 = Gathers, 2=Jaime, 3=Arya

		# TODO: This should update based on units
		if self.gold > 10 + len([u for u in self.units if u.owner == 'ME']):
			self.actions.append(f'TRAIN 1 {train_pos.x} {train_pos.y}')


	def init(self):
		# Unused in Wood 3
		number_mine_spots = int(input())
		for i in range(number_mine_spots):
			x, y = [int(j) for j in input().split()]

	def update(self):
		self.units.clear()
		self.buildings.clear()
		self.actions.clear()

		self.gold = int(input())
		self.income = int(input())
		self.opponent_gold = int(input())
		self.opponent_income = int(input())

		for i in range(12):
			line = input()
			self.board.append(line)
			print(line, file=sys.stderr)

		building_count = int(input())
		for i in range(building_count):
			owner, building_type, x, y = [int(j) for j in input().split()]
			self.buildings.append(Building(owner, building_type, x, y))

		unit_count = int(input())
		for i in range(unit_count):
			owner, unit_id, level, x, y = [int(j) for j in input().split()]
			self.units.append(Unit(owner, unit_id, level, x, y))

	def build_output(self):
		# TODO "core" of the AI
		self.train_units()
		self.move_units()
		

	def output(self):
		self.actions.append(self.message)
		if self.actions:
			print(';'.join(self.actions))
		else:
			print('WAIT')


g = Game()

g.init()
while True:
	g.update()
	g.build_output()
	g.output()