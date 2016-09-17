#Topics: Loops, Distances, Medians
#Goal: Connect houses using the minimum amount of cable possible
#Score: 100%
#Notes: The trick to this puzzle which made it easier to complete was to find the average y value (West-East) then use a few modifiers to determine which y value used the least amount of cord

import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

houseX = []
houseY = []

n = int(raw_input())
for i in xrange(n):
	x, y = [int(j) for j in raw_input().split()]
	print >> sys.stderr, "(%i,%i)" % (x, y)
	houseX.append(x)
	houseY.append(y)

#Originally I used average to find the most likely spot, I then converted over to median
houseY.sort()
origWireY = houseY[len(houseY)/2]

#Put the width in our answer
minAnswer = 99999999999999999999999999999999999999999999999999999999999999999999999999999999
manipulators = [1,0,-1,2,-2,3,-3,4,-4]
for manipulator in manipulators:
	wireY = origWireY+manipulator
	
	answer = max(houseX)-min(houseX)
	for y in houseY:
		answer+=abs(y-wireY)

	print >> sys.stderr, "%i gives us %i" % (manipulator, answer)
	if answer < minAnswer:
		minAnswer = answer

print int(minAnswer)
