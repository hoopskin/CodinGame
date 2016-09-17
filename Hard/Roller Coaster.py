#Topics: Simulation, Dynamic Programming
#Goal: Given a queue of groups, the max size of individuals that can fit simulatenously on a coaster, and a set number of rides, determine the number of individuals that will go on the ride
#Score: 100%
#Note: One thing to note about this puzzle is that routinely you won't fill up the ride to 100% due to the groups not splitting up.
#I also learned with the larger data sets that (in order to complete it in the allotted processing time), I was required to create a 'memory' of sorts for the system.
#This was due to the max number of spots on the ride and number of times the ride could operate were 10^7.
#This 'memory' was done by determining if I had seen this index in the line before and (since the result would always be the same for the same index) be able to simply add the count of individuals that would go on the ride that cycle and what the next index would be.


import sys, math

#L = Number of places on ride
#C = Number of times it can run in a day
#N = Number of groups
#Pi = Number of people in a group (iterates)
L, C, N = [int(i) for i in raw_input().split()]

groupsArray = []
idx = 0
ride = 0

memory = {}
for i in xrange(N):
    Pi = int(raw_input())
    groupsArray.append(Pi)

answer = 0
#While it can run again
while C > 0:
	#Reset origIdx and ride
	origIdx = idx
	ride = 0

	#If this index is in memory
	try:
		answer+=memory[idx][0]
		#Increase answer

		#Move Idx to next Idx
		idx = memory[idx][1]

	#Else, discover answer
	except KeyError:
		rideAmount = 0
		#While there is still space
		while ride+groupsArray[idx]<=L:
			#Add people to the ride
			ride+=groupsArray[idx]
	
			#Take their money
			answer+=groupsArray[idx]

			#Add to ride amount
			rideAmount+=groupsArray[idx]
	
			#Using an index instead of actually modifying the list as it's easier and faster with the same result
			idx = int((idx+1)%len(groupsArray))
	
			#If there's no one left in line, you're done adding people to the ride
			if idx == origIdx:
				break
	
		#Ride the ride!
	
		#Add them back into the queue (No need for this since idx loops back anyway)

		#Put into memory
		memory[origIdx] = [rideAmount, idx]
	
	#Reduce run time
	C-=1

#Print answer
print answer