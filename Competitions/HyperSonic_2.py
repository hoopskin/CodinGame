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
emptyBox = '0'
rangeBox = '1'
bombBox = '2'
wall = 'X'
locsToGet = 1
roundsRemaining = 200

#Bomb Range = 3
#Bomb hitting bomb means bomb explodes (say bomb again. I dare you.)

def getImpact(x, y):
	#TOOD: Need to realize difference between different boxes.
	#NOTE: Items appear on map at floor. entityObjects will have it in the list though
	impact = 0
	#North
	for i in range(1,me.param_2):
		if y-i < 0:
			break
		else:
			if gameMap[y-i][x] != floor:
				if gameMap[y-i][x] != wall:
					impact+=1
				break

	#South
	for i in range(1,me.param_2):
		if y+i >= height:
			break
		else:
			if gameMap[y+i][x] != floor:
				if gameMap[y+i][x] != wall:
					impact+=1
				break

	#East
	for i in range(1,me.param_2):
		if x+i >= width:
			break
		else:
			if gameMap[y][x+i] != floor:
				if gameMap[y][x+i] != wall:
					impact+=1
				break

	#West
	for i in range(1,me.param_2):
		if x-i < 0:
			break
		else:
			if gameMap[y][x-i] != floor:
				if gameMap[y][x-i] != wall:
					impact+=1
				break

	return impact

def getCurLoc():
	for e in entityObjects:
		if e.entity_type == 0 and e.owner == my_id:
			return e.x, e.y

def fillTempMap(x, y):
	global tmpMap, possibleLocations
	possibleLocations.append([x,y])
	#North
	#If it's in the map
	if y-1 > 0:
		#and is a dot
		if tmpMap[y-1][x] == ".":
			#Visit it and fill
			tmpMap[y-1][x] = "!"
			fillTempMap(x, y-1)

	#South
	if y+1 < height:
		if tmpMap[y+1][x] == ".":
			tmpMap[y+1][x] = "!"
			fillTempMap(x, y+1)

	#East
	if x+1 < width:
		if tmpMap[y][x+1] == ".":
			tmpMap[y][x+1] = "!"
			fillTempMap(x+1, y)

	#West
	if x-1 > 0:
		if tmpMap[y][x-1] == ".":
			tmpMap[y][x-1] = "!"
			fillTempMap(x-1, y)

def getColumnValues(data, idx):
	"""Gets all the values from one column into an array. Returns that array"""
	rtn = []
	for row in data:
		rtn.append(row[idx])
	return rtn

def sortByColumnIdx(data, idx):
	valsToSortOn = getColumnValues(data, idx)
	
	#Remove Duplicates
	valsToSortOn = list(set(valsToSortOn))
	
	#Sort
	valsToSortOn.sort()
	valsToSortOn.reverse()

	rtn = []
	#For each value to sort on
	for val in valsToSortOn:
		#1 to account for headers
		i = 0
		idxsToRemove = []
		while i < len(data):
			row = data[i]
			if row[idx] == val:
				rtn.append(row)
				idxsToRemove.append(i)
			i+=1
		#Sort & Reverse to ensure that the index for the objects we want to delete don't move
		idxsToRemove.sort()
		idxsToRemove.reverse()
		for i in idxsToRemove:
			data.remove(data[i])

	return rtn

def getBestLoc():
	global possibleLocations

	#TODO: Return x best where x = number of bombs I can drop
	x = me.x
	y = me.y
	maxImpact = 0
	maxX = -1
	maxY = -1

	fillTempMap(me.x, me.y)

	#Remove my bombs from possible spots
	for e in getMyBombs():
		try:
			possibleLocations.remove([e.x, e.y])
		except(ValueError):
			pass

	i = 0
	while i < len(possibleLocations):
		loc = possibleLocations[i]
		possibleLocations[i].append(getImpact(loc[0], loc[1]))
		i+=1

	possibleLocations = sortByColumnIdx(possibleLocations, -1)

	return possibleLocations[:locsToGet]

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
						if gameMap[e.y-i][e.x] != wall:
							gameMap[e.y-i][e.x] = floor
						break

			#South
			for i in range(1,e.param_2):
				if e.y+i >= height:
					break
				else:
					if gameMap[e.y+i][e.x] != floor:
						if gameMap[e.y+i][e.x] != wall:
							gameMap[e.y+i][e.x] = floor
						break

			#East
			for i in range(1,e.param_2):
				if e.x+i >= width:
					break
				else:
					if gameMap[e.y][e.x+i] != floor:
						if gameMap[e.y][e.x+i] != wall:
							gameMap[e.y][e.x+i] = floor
						break

			#West
			for i in range(1,e.param_2):
				if e.x-i < 0:
					break
				else:
					if gameMap[e.y][e.x-i] != floor:
						if gameMap[e.y][e.x-i] != wall:
							gameMap[e.y][e.x-i] = floor
						break

def getMyBombs():
	rtn = []
	for e in entityObjects:
		if e.entity_type == 1 and e.owner == my_id:
			rtn.append(e)
	return rtn

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
	tmpMap = []
	possibleLocations = []
	for i in range(height):
		row = input()
		#print(row, file=sys.stderr)
		gameMap.append(list(row))
		tmpMap.append(list(row))
	entities = int(input())
	for i in range(entities):
		entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
		entityObjects.append(Entity(entity_type, owner, x, y, param_1, param_2))
		if entity_type == 0 and owner == my_id:
			me = entityObjects[-1]
			locsToGet = max(locsToGet, me.param_1)

	#bombTheMap()

	bestLocs = getBestLoc()
	print(bestLocs, file=sys.stderr)
	bestX = bestLocs[0][0]
	bestY = bestLocs[0][1]
	myX, myY = me.x, me.y
	x, y = -1, -1
	message = ""
	
	#If there are no items, go to best spot
	#TODO: If I have an un-beatable score (the difference is too big to surmount), then I should hide and not die
	#TODO: Need to go bomb somewhere if I still have available bombs
	items = getItems()
	if len(items) == 0:
		x, y = bestX, bestY
		message = "Bombing!"
	else:
		#Is best or item closer?
		itemDist = abs(math.hypot(x - items[0].x, y - items[0].y))
		bestDist = abs(math.hypot(x - bestX, y - bestY))
		if abs(math.hypot(x - items[0].x, y - items[0].y)) < abs(math.hypot(x - bestX, y - bestY)):
			x, y = items[0].x, items[0].y
			message = "Item's better!"
		else:
			x, y = bestX, bestY
			message = "Bombing's better!"

	if bestX == myX and bestY == myY:
		action = "BOMB"
	else:
		action = "MOVE"

	print("%s %i %i %s" % (action, x, y, message))
