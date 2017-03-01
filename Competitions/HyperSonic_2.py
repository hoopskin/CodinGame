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

itemImpact = -1
boxImpactDict = {
emptyBox:1,
rangeBox:2,
bombBox:3}

def getImpact(x, y, wantLocations):
	#NOTE: Items appear on map at floor. entityObjects will have it in the list though
	impact = 0
	impactedLocations = [[x,y]]
	#North
	for i in range(1,me.param_2):
		if y-i < 0:
			break
		else:
			impactedLocations.append([x,(y-i)])
			if gameMap[y-i][x] != floor:
				if [x,y] in itemLocs:
					impact+=itemImpact
					break
				if gameMap[y-i][x] == wall:
					break
				else:
					impact+=boxImpactDict[gameMap[y-i][x]]
					break

	#South
	for i in range(1,me.param_2):
		if y+i >= height:
			break
		else:
			impactedLocations.append([x,(y+i)])
			if gameMap[y+i][x] != floor:
				if [x,y] in itemLocs:
					impact+=itemImpact
					break
				if gameMap[y+i][x] == wall:
					break
				else:
					impact+=boxImpactDict[gameMap[y+i][x]]
					break

	#East
	for i in range(1,me.param_2):
		if x+i >= width:
			break
		else:
			impactedLocations.append([(x+i),y])
			if gameMap[y][x+i] != floor:
				if [x,y] in itemLocs:
					impact+=itemImpact
					break
				if gameMap[y][x+i] == wall:
					break
				else:
					impact+=boxImpactDict[gameMap[y][x+i]]
					break

	#West
	for i in range(1,me.param_2):
		if x-i < 0:
			break
		else:
			impactedLocations.append([(x-i),y])
			if gameMap[y][x-i] != floor:
				if [x,y] in itemLocs:
					impact+=itemImpact
					break
				if gameMap[y][x-i] == wall:
					break
				else:
					impact+=boxImpactDict[gameMap[y][x-i]]
					break

	if wantLocations:
		return impactedLocations
	else:
		return impact

def getCurLoc():
	for e in entityObjects:
		if e.entity_type == 0 and e.owner == my_id:
			return e.x, e.y

#TODO: Use something like this to find the closest non-bomb affected square
def fillTempMap(x, y):
	global tmpMap, possibleLocations
	tmpMap[y][x] = "!"
	possibleLocations.append([x,y])
	#North
	#If it's in the map
	if y-1 >= 0:
		#and is a dot
		if tmpMap[y-1][x] == "." and ([x, y-1] not in bombLocs):
			#Visit it and fill
			fillTempMap(x, y-1)

	#South
	if y+1 < height:
		if tmpMap[y+1][x] == "." and ([x, y+1] not in bombLocs):
			fillTempMap(x, y+1)

	#East
	if x+1 < width:
		if tmpMap[y][x+1] == "." and ([x+1, y] not in bombLocs):
			fillTempMap(x+1, y)

	#West
	if x-1 >= 0:
		if tmpMap[y][x-1] == "." and ([x-1, y] not in bombLocs):
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
	global possibleLocations, dangerLocations

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
			#Remove bomb-affected places as well (does mean that we'll ignore it even if bomb will go off before arriving)
		for loc in getImpact(e.x, e.y, True):
			dangerLocations.append([loc[0],loc[1]])

	try:
		possibleLocations.remove([0,0])
	except(ValueError):
		pass

	for d in dangerLocations:
		try:
			possibleLocations.remove([d[0],d[1]])
		except(ValueError):
			pass

	i = 0
	while i < len(possibleLocations):
		loc = possibleLocations[i]
		possibleLocations[i].append(getImpact(loc[0], loc[1], False))
		i+=1

	possibleLocations = sortByColumnIdx(possibleLocations, -1)
	if possibleLocations[0][0] == me.x and possibleLocations[0][1] == me.y:
		for b in getBombs():
			if possibleLocations[0][0] == b.x and possibleLocations[0][1] == b.y:
				possibleLocations = possibleLocations[1:]

	return possibleLocations[:locsToGet]

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
	dangerLocations = []

	#Get Round data
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

	#Capture items and their locations
	items = getItems()
	itemLocs = []
	for i in items:
		itemLocs.append([i.x, i.y])

	bombs = getBombs()
	bombLocs = []
	for b in bombs:
		bombLocs.append([b.x, b.y])

	#Determine the X best locations where X = max of bombs available or 1
	try:
		bestLocs = getBestLoc()
	except(IndexError):
		#There's no where to go, but hopefully there will be
		print("MOVE %i %i Wait and die..." % (lastAction[0], lastAction[1]))
		continue

	print("Length: %i" % (me.param_2), file=sys.stderr)
	print(bestLocs, file=sys.stderr)
	
	message = ""
	action = ""
	x, y = -1, -1

	#If there's nothing better than what I was going for, keep going for it
	if lastAction[-1] >= bestLocs[0][-1]:
		message = "Old: %i > %i" % (lastAction[-1], bestLocs[0][-1])
		x, y = lastAction[0], lastAction[1]
	else:
		message = "New: %i < %i" % (lastAction[-1], bestLocs[0][-1])
		x, y = bestLocs[0][0], bestLocs[0][1]

	print("DangerLocs: "+str(dangerLocations), file=sys.stderr)
	#If old is danger, choose new
	if [x, y] in dangerLocations:
		message = "I want to live!"
		x, y = bestLocs[0][0], bestLocs[0][1]

	#If there's a closer item, get that instead
	if len(items) > 0:
		shortestDist = abs(math.hypot(me.x - x, me.y - y))
		for i in items:
			if [i.x, i.y, getImpact(i.x, i.y, False)] in possibleLocations:
				itemDist = abs(math.hypot(me.x - i.x, me.y - i.y))
				if itemDist < shortestDist:
					message = "Items rule!"
					shortestDist = itemDist
					x, y = i.x, i.y

	#If the impact of here is > 2 OR I'm at the best spot, BOMB. Else MOVE
	if (me.x == x and me.y == y and message != "Items rule!") or (getImpact(x,y, False) > 3 and abs(math.hypot(me.x - x, me.y - y)) > 2):
		action = "BOMB"
	else:
		action = "MOVE"

	if lastCommand == "BOMB":
		action = "MOVE"
	print("Last Action: "+str(lastAction), file=sys.stderr)
	print("Current Action: "+str([x, y, getImpact(x,y, False)]), file=sys.stderr)

	lastCommand = action
	lastAction = [x, y, getImpact(x,y, False)]
	lastMessage = message

	#TODO: If they haven't moved in awhile and I'm winning, run out the clock?
	if roundsRemaining == 200 and y == 0 and action == "BOMB":
		action = "MOVE"
	print("%s %i %i %s" % (action, x, y, message))
	roundsRemaining-=1