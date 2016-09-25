import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

mapData = []
coordsToTest = []
tmpMapData = []
debugging = False

def fillLakeArea(x, y):
	global tmpMapData
	#Change this spot to a "."
	floodQueue = [[x,y]]
	
	while len(floodQueue) > 0:
		curX = floodQueue[0][0]
		curY = floodQueue[0][1]
		floodQueue.pop(0)
		
		tmpMapData[curY][curX] = "."

		#Check north for lake
		if y-1 >= 0 and tmpMapData[y-1][x] == "O":
			fillLakeArea(x, y-1)
		#Check east for lake
		if x+1 < len(tmpMapData[0]) and tmpMapData[y][x+1] == "O":
			fillLakeArea(x+1, y)
		#Check south for lake
		if y+1 < len(tmpMapData) and tmpMapData[y+1][x] == "O":
			fillLakeArea(x, y+1)
		#Check west for lake
		if x-1 >= 0 and tmpMapData[y][x-1] == "O":
			fillLakeArea(x-1, y)

def detLakeArea():
	rtn = 0
	for row in tmpMapData:
		for val in row:
			if val == ".":
				rtn+=1
	return rtn

l = int(input())
h = int(input())
for i in range(h):
	row = input()
	mapData.append(list(row))
n = int(input())
for i in range(n):
	x, y = [int(j) for j in input().split()]
	coordsToTest.append([x,y])
for i in range(n):
	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)

	#Reset tempMap
	#tmpMapData = mapData[:]
	tmpMapData=[]
	for row in mapData:
		tmpMapData.append(row[:])

	#Get Coordinates
	x = coordsToTest[i][0]
	y = coordsToTest[i][1]
	#If that location is land (#), then zero
	if mapData[y][x] == "#":
		print(0)
	else:
		try:
			fillLakeArea(x, y)
		except Exception as e:
			print(e, file=sys.stderr)
		print(detLakeArea())