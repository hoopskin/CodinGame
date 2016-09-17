#Topics: Conditions
#Goal: Given a map of tunnels, determine where Indy will fall.
#Score: 100%
#Notes: I usually find condition puzzles pretty straight-forward, which allows for more creativity in HOW I solve the problem.
#With this puzzle, I decided to use a list of dictionaries for the following reasons:
#1) You were to be given the 'type' of square that Indy is on currently (0-13)
#2) For each one, Indy could come from a certain way and that would determine where he would go next (e.g. if it's a vertical piece, Indy would come in from TOP and leave out of BOTTOM)
#While this style requires some pre-work of creating the correct list of dictionaries, it make getting dirToGo very simple

import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: number of columns.
# h: number of rows.
typeMap = []

w, h = [int(i) for i in raw_input().split()]
for i in xrange(h):
	line = raw_input()  # represents a line in the grid and contains W integers. Each integer represents one room of a given type.
	typeMap.append(line.split())

ex = int(raw_input())  # the coordinate along the X axis of the exit (not useful for this first mission, but must be read).

directionDict = [{},{"LEFT": "DOWN", "TOP": "DOWN", "RIGHT": "DOWN"},{"LEFT": "RIGHT", "RIGHT": "LEFT"},{"TOP": "DOWN"},{"TOP": "LEFT", "RIGHT": "DOWN"},{"TOP": "RIGHT", "LEFT": "DOWN"},{"TOP": "DEATH?", "LEFT": "RIGHT", "RIGHT": "LEFT"},{"TOP": "DOWN", "RIGHT": "DOWN"},{"LEFT": "DOWN", "RIGHT": "DOWN"},{"TOP": "DOWN", "LEFT": "DOWN"},{"TOP": "LEFT", "LEFT": "DEATH?"},{"TOP": "RIGHT", "RIGHT": "DEATH?"},{"RIGHT": "DOWN"},{"LEFT": "DOWN"}]

# game loop
while True:
	xi, yi, pos = raw_input().split()
	xi = int(xi)
	yi = int(yi)

	print >> sys.stderr, "Pos: "+pos
	print >> sys.stderr, "X Y: %s %s" % (xi, yi)

	curType = int(typeMap[yi][xi])
	print >> sys.stderr, "Type: " + str(curType)

	dirToGo = directionDict[curType][pos]
	print >> sys.stderr, "Dir To Go: " + dirToGo

	if dirToGo == "LEFT":
		xi-=1
	elif dirToGo == "RIGHT":
		xi+=1
	else:
		yi+=1

	# One line containing the X Y coordinates of the room in which you believe Indy will be on the next turn.
	print "%i %i"%(xi, yi)
