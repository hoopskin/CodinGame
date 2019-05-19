import sys, math, random

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

	def det_unit_movement(self, unit):
		unitX = unit.pos.x
		unitY = unit.pos.y
		oppHQPos = self.get_opponent_HQ().pos

		#If you are right next to the HQ, kill them
		for offset in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
			newX = unitX+offset[0]
			newY = unitY+offset[1]
			if Position(newX, newY) == oppHQPos:
				return Position(newX, newY)


		#If you can kill something next to you, do that
		oppUnitPositions = [u.pos for u in self.units if u.owner == OPPONENT]
		for offset in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
			newX = unitX+offset[0]
			newY = unitY+offset[1]
			if Position(newX, newY) in oppUnitPositions:
				return Position(newX, newY)

		#If there's a free spot next to you (looking clock-wise starting at N), take it
		for offset in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
			newX = unitX+offset[0]
			newY = unitY+offset[1]

			if (newX < 0) or (newY < 0) or (newX > 11) or (newY > 11):
				#Invalid so skip
				continue

			try:
				spot = self.board[newY][newX]
				if spot in [NEUTRAL, CAPTURED_OPP, INACTIVE_OPP]:
					debugline = "%i saw NEUTRAL at (%i, %i)" % (unit.id, newX, newY)
					print(debugline, file=sys.stderr)
					return Position(newX, newY)
			except(IndexError):
				pass

		#If you can't do anything, just go towards HQ
		#return self.get_opponent_HQ().pos
		if self.get_opponent_HQ().pos.x == 0:
			#Need to go North / West
			if random.random() < .5:
				#North
				return Position(unitX, unitY-1)
			else:
				#West
				return Position(unitX-1, unitY)
		else:
			#Need to go South / East
			if random.random() < .5:
				#South
				return Position(unitX, unitY+1)
			else:
				#West
				return Position(unitX+1, unitY)

	def move_units(self):
		#Kill ability: 1=NA, 2=1, 3=All
		#Ergo, 1 = Gathers, 2=Jaime, 3=Arya
		unitList = [u for u in self.units if u.owner == ME]
		for unit in unitList:
			loc = self.det_unit_movement(unit)
			if (loc.x < 0) or (loc.y < 0) or (loc.x > 11) or (loc.y > 11):
				loc = self.get_opponent_HQ().pos

			self.actions.append(f'MOVE {unit.id} {loc.x} {loc.y}')

	def get_train_position(self):
		# TODO: this just puts a unit at the HQ. Safe, but fix
		try:
			units = [u for u in self.units if u.owner == ME]
			oldestUnit = [u for u in units if u.id == min([u.id for u in units])][0]

			while True:
				offsetOptions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
				randomOffset = random.choice(offsetOptions)
				offsetOptions.remove(randomOffset)

				trainX = oldestUnit.pos.x+randomOffset[0]
				trainY = oldestUnit.pos.y+randomOffset[1]
				if (trainX < 0) or (trainY < 0) or (trainX > 11) or (trainY > 11) or (Position(trainX, trainY) in [u.pos for u in self.units]):
					continue
				else:
					break

			return Position(oldestUnit.pos.x+randomOffset[0], oldestUnit.pos.y+randomOffset[1])		
		except(IndexError):
			hq = self.get_my_HQ()

			if hq.pos.x == 0:
				return Position(0, 1)
			return Position(11, 10)


	def train_units(self):
		train_pos = self.get_train_position()
		myUpkeep = sum([u.upkeep for u in self.units if u.owner == 'ME'])
		#Recruit Costs: 1=10, 2=20, 3=30
		#Kill ability: 1=NA, 2=1, 3=All
		#Ergo, 1 = Gathers, 2=Jaime, 3=Arya
		#upkeep = {1:1, 2:4, 3:20}

		# TODO: This should update based on units
		if (self.gold > 30 + myUpkeep) and (self.income >= 20):
			self.actions.append(f'TRAIN 3 {train_pos.x} {train_pos.y}')
			self.gold -= 30
			self.income -= 20

		if (self.gold > 20 + myUpkeep) and (self.income >= 4):
			self.actions.append(f'TRAIN 2 {train_pos.x} {train_pos.y}')
			self.gold -= 20
			self.income -= 4

		if (self.gold > 10 + myUpkeep) and (self.income >= 1):
			self.actions.append(f'TRAIN 1 {train_pos.x} {train_pos.y}')
			self.gold -= 10
			self.income -= 1


	def init(self):
		# Unused in Wood 3
		number_mine_spots = int(input())
		for i in range(number_mine_spots):
			x, y = [int(j) for j in input().split()]

	def update(self):
		self.units.clear()
		self.buildings.clear()
		self.actions.clear()
		self.board.clear()

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