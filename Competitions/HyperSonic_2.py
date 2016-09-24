import sys
import math

class Entity(object):
	def __init__(self, entity_type, owner, x, y, param_1, param_2):
		#entity_type = id of the player (0 for player or 1 for bomb)
		#owner = id of the bomb owner
		#x = x
		#y = y
		#param_1 = Players: Numbers of bombs a player can still place. Bombs: Rounds left until explosion
		#param_2 = Players: Explosion range of player's bombs. Bombs: Explosion range.
		super(Entity, self).__init__()
		self.entity_type = entity_type
		self.owner = owner
		self.x = x
		self.y = y
		self.param_1 = param_1
		self.param_2 = param_2
		

width, height, my_id = [int(i) for i in input().split()]
floor = '.'
box = '0'
roundsRemaining = 200

#Bomb Range = 3
#Bomb hitting bomb means bomb explodes (say bomb again. I dare you.)

def getImpact(x, y):
	impact = 0
	#North
	for i in range(1,me.param_2):
		if y-i < 0:
			break
		else:
			if gameMap[y-i][x] != floor:
				impact+=1
				break

	#South
	for i in range(1,me.param_2):
		if y+i >= height:
			break
		else:
			if gameMap[y+i][x] != floor:
				impact+=1
				break

	#East
	for i in range(1,me.param_2):
		if x+i >= width:
			break
		else:
			if gameMap[y][x+i] != floor:
				impact+=1
				break

	#West
	for i in range(1,me.param_2):
		if x-i < 0:
			break
		else:
			if gameMap[y][x-i] != floor:
				impact+=1
				break

	return impact

def getMyBombObj():
	for e in entityObjects:
		if e.entity_type == 1 and e.owner == my_id:
			return e

def getCurLoc():
	for e in entityObjects:
		if e.entity_type == 0 and e.owner == my_id:
			return e.x, e.y

def getBestLoc():
	x = 0
	y = 0
	maxImpact = 0
	maxX = -1
	maxY = -1
	myBomb = getMyBombObj()
	for x in range(width):
		for y in range(height):
			if gameMap[y][x] == floor:
				impact = getImpact(x, y)
				if impact > maxImpact and (myBomb == None or x != myBomb.x and y != myBomb.y):
					maxX = x
					maxY = y
					maxImpact = impact
	return maxX, maxY

def bombTheMap():
	global gameMap
	for e in entityObjects:
		if entity_type == 1:
			#North
			for i in range(1,e.param_2):
				if e.y-i < 0:
					break
				else:
					if gameMap[e.y-i][e.x] != floor:
						gameMap[e.y-i][e.x] = floor
						break

			#South
			for i in range(1,e.param_2):
				if e.y+i >= height:
					break
				else:
					if gameMap[e.y+i][e.x] != floor:
						gameMap[e.y+i][e.x] = floor
						break

			#East
			for i in range(1,e.param_2):
				if e.x+i >= width:
					break
				else:
					if gameMap[e.y][e.x+i] != floor:
						gameMap[e.y][e.x+i] = floor
						break

			#West
			for i in range(1,e.param_2):
				if e.x-i < 0:
					break
				else:
					if gameMap[e.y][e.x-i] != floor:
						gameMap[e.y][e.x-i] = floor
						break

def getItems():
	rtn = []
	for e in entityObjects:
		if e.entity_type == 2:
			rtn.append(e)

	return rtn

# game loop
while True:
	entityObjects = []
	gameMap = []
	for i in range(height):
		row = input()
		gameMap.append(list(row))
	entities = int(input())
	for i in range(entities):
		entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
		entityObjects.append(Entity(entity_type, owner, x, y, param_1, param_2))
		if entity_type == 0 and owner == my_id:
			me = entityObjects[-1]

	#bombTheMap()

	bestX, bestY = getBestLoc()
	myX, myY = me.x, me.y
	x, y = -1, -1
	
	#If there are no items, go to best spot
	items = getItems()
	if len(items) == 0:
		x, y = bestX, bestY
	else:
		#Is best or item closer?
		if abs(math.hypot(x - items[0].x, y - items[0].y)) < abs(math.hypot(x - bestX, y - bestY)):
			x, y = items[0].x, items[0].y
		else:
			x, y = bestX, bestY

	if bestX == myX and bestY == myY:
		action = "BOMB"
	else:
		action = "MOVE"

	if x == -1:
		print("%i %i" % (getBestLoc()), file=sys.stderr)
		print(gameMap, file=sys.stderr)

	print("%s %i %i" % (action, x, y))
