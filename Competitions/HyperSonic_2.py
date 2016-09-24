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
gameMap = []
floor = '.'
box = '0'
roundsRemaining = 200

#Bomb Range = 3
#Bomb hitting bomb means bomb explodes (say bomb again. I dare you.)

def getImpact(x, y):
	impact = 0
	#North
	for i in range(1,4):
		if y-i < 0:
			break
		else:
			if gameMap[y-i][x] == box:
				impact+=1
				break

	#South
	for i in range(1,4):
		if y+i >= height:
			break
		else:
			if gameMap[y+i][x] == box:
				impact+=1
				break

	#East
	for i in range(1,4):
		if x+i >= width:
			break
		else:
			if gameMap[y][x+i] == box:
				impact+=1
				break

	#West
	for i in range(1,4):
		if x-i < 0:
			break
		else:
			if gameMap[y][x-i] == box:
				impact+=1
				break

	return impact

def getBestLoc():
	x = 0
	y = 0
	maxImpact = 0
	maxX = -1
	maxY = -1
	for x in range(width):
		for y in range(height):
			impact = getImpact(x, y)
			if impact > maxImpact:
				maxX = x
				maxY = y
				maxImpact = impact
	return maxX, maxY

def getMyBombObj():
	for e in entityObjects:
		if e.entity_type == 1 and e.owner = my_id:
			return e

# game loop
while True:
	entityObjects = []
	for i in range(height):
		row = input()
		gameMap.append(list(row))
	entities = int(input())
	for i in range(entities):
		entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
		entityObjects.append(Entity(entity_type, owner, x, y, param_1, param_2))

	bestX, bestY = getBestLoc()
	print("BOMB %i %i" % (bestX, bestY))