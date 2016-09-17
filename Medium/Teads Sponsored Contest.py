#Topics: Memoization, Graphs
#Goal: Given a network of individuals, find the minimal number of steps required for the message to propogate to everyone
#Score: 100%
#Notes: The way to solve this one is to take your dictionary of connections and perform the following loop
#1) Find the exit nodes (the ones with only one connection)
#2) Remove them from your connection dictionary
#3) Increase your step counter
#4) Repeat until empty

#The idea behind this is to go from the outside in instead of searching for a 'middle' of the network

import sys
import math

def findExitNodes():
	rtn = []
	for key in cnctDict.keys():
		if len(cnctDict[key]) < 2:
			rtn.append(key)

	return rtn

cnctDict = {}

n = int(raw_input())  # the number of adjacency relations
print >> sys.stderr, n
for i in xrange(n):
	# xi: the ID of a person which is adjacent to yi
	# yi: the ID of a person which is adjacent to xi
	xi, yi = [int(j) for j in raw_input().split()]
	try:
		cnctDict[xi].append(yi)
	except KeyError:
		cnctDict[xi] = [yi]
	
	try:
		cnctDict[yi].append(xi)
	except KeyError:
		cnctDict[yi] = [xi]

steps = 1
#While there's still keys
while len(cnctDict.keys()) > 1:
	print >> sys.stderr, str(steps)+" "+str(cnctDict)
	#Find the ones with only 1 connection
	exitNodes = set(findExitNodes())
	#Remove each key from all the values
	for key in cnctDict.keys():
		cnctDict[key] = list(set(cnctDict[key])-exitNodes)
	for node in exitNodes:
		#Delete key
		cnctDict.pop(node)
	#Increase steps
	steps+=1


# The minimal amount of steps required to completely propagate the advertisement
print str(steps-1)