import sys
import math

class Entity(object):
	def __init__(self, entity_type, owner, x, y, param_1, param_2):
		#entity_type = id of the player (0 for player 1 for bomb, 2 for item)
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
				if [x,y] in itemLocs:
					impact-=1
					break
				if gameMap[y-i][x] == wall:
					break
				else:
					impact+=1+int(gameMap[y-i][x])
					break

	#South
	for i in range(1,me.param_2):
		if y+i >= height:
			break
		else:
			if gameMap[y+i][x] != floor:
				if [x,y] in itemLocs:
					impact-=1
					break
				if gameMap[y+i][x] == wall:
					break
				else:
					impact+=1+int(gameMap[y+i][x])
					break

	#East
	for i in range(1,me.param_2):
		if x+i >= width:
			break
		else:
			if gameMap[y][x+i] != floor:
				if [x,y] in itemLocs:
					impact-=1
					break
				if gameMap[y][x+i] == wall:
					break
				else:
					impact+=1+int(gameMap[y][x+i])
					break

	#West
	for i in range(1,me.param_2):
		if x-i < 0:
			break
		else:
			if gameMap[y][x-i] != floor:
				if [x,y] in itemLocs:
					impact-=1
					break
				if gameMap[y][x-i] == wall:
					break
				else:
					impact+=1+int(gameMap[y][x-i])
					break

	return impact

def getCurLoc():
	for e in entityObjects:
		if e.entity_type == 0 and e.owner == my_id:
			return e.x, e.y

def fillTempMap(x, y):
	global tmpMap, possibleLocations
	tmpMap[y][x] = "!"
	possibleLocations.append([x,y])
	#North
	#If it's in the map
	if y-1 >= 0:
		#and is a dot
		if tmpMap[y-1][x] == ".":
			#Visit it and fill
			fillTempMap(x, y-1)

	#South
	if y+1 < height:
		if tmpMap[y+1][x] == ".":
			fillTempMap(x, y+1)

	#East
	if x+1 < width:
		if tmpMap[y][x+1] == ".":
			fillTempMap(x+1, y)

	#West
	if x-1 >= 0:
		if tmpMap[y][x-1] == ".":
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

	#Remove bombs from possible spots
	for e in getBombs():
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
	if possibleLocations[0][0] == me.x and possibleLocations[0][1] == me.y:
		for b in getBombs():
			if possibleLocations[0][0] == b.x and possibleLocations[0][1] == b.y:
				possibleLocations = possibleLocations[1:]

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

def getBombs():
	rtn = []
	for e in entityObjects:
		if e.entity_type == 1:
			rtn.append(e)

	return rtn

def matchesLastBestLocs(tmpBestLocs):
	for i in lastBestLocs:
		try:
			tmpBestLocs.remove(i)
		except(ValueError):
			return False
	return True

# game loop
lastCommand = ""
lastAction = [-1,-1,-1]
lastBestLocs = []
while True:
	#Reset any necessary variables
	entityObjects = []
	gameMap = []
	tmpMap = []
	possibleLocations = []

	#Get Round data
	for i in range(height):
		row = input()
		gameMap.append(list(row))
		tmpMap.append(list(row))

	entities = int(input())
	for i in range(entities):
		entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
		entityObjects.append(Entity(entity_type, owner, x, y, param_1, param_2))
		if entity_type == 0 and owner == my_id:
			me = entityObjects[-1]
			locsToGet = max(locsToGet, me.param_1)

	#Capture items and their locations
	items = getItems()
	itemLocs = []
	for i in items:
		itemLocs.append([i.x, i.y])

	#Determine the X best locations where X = max of bombs available or 1
	bestLocs = getBestLoc()

	print("Length: %i" % (me.param_2), file=sys.stderr)
	print(bestLocs, file=sys.stderr)
	
	message = ""
	action = ""
	x, y = -1, -1

	#If there's nothing better than what I was going for, keep going for it
	if lastAction[-1] > bestLocs[0][-1]:
		message = "Old: %i > %i" % (lastAction[-1], bestLocs[0][-1])
		x, y = lastAction[0], lastAction[1]
	else:
		message = "New: %i < %i" % (lastAction[-1], bestLocs[0][-1])
		x, y = bestLocs[0][0], bestLocs[0][1]

	#If there's a closer item, get that instead
	if len(items) > 0:
		shortestDist = abs(math.hypot(me.x - x, me.y - y))
		for i in items:
			itemDist = abs(math.hypot(me.x - i.x, me.y - i.y))
			if itemDist < shortestDist:
				message = "Items rule!"
				shortestDist = itemDist
				x, y = i.x, i.y

	#If the impact of here is > 2 OR I'm at the best spot, BOMB. Else MOVE
	if (me.x == x and me.y == y and message != "Items rule!") or getImpact(x,y) > 3:
		action = "BOMB"
	else:
		action = "MOVE"

	if lastCommand == "BOMB":
		action = "MOVE"
	print("Last Action: "+str(lastAction), file=sys.stderr)
	print("Current Action: "+str([x, y, getImpact(x,y)]), file=sys.stderr)

	lastCommand = action
	lastAction = [x, y, getImpact(x,y)]
	lastMessage = message

	#TODO: If they haven't moved in awhile and I'm winning, run out the clock?
	print("%s %i %i %s" % (action, x, y, message))
