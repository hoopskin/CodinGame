import sys, math
import random as r
print("Debug", file=sys.stderr)


class Entity(object):
	def __init__(self, entity_id, owner, entity_type, cyborgCount=0, factoryProduction=0, fromFactory=-1, toFactory=-1, troopSize=-1, distanceToTarget=-1):
		super(Entity, self).__init__()
		self.entity_id = entity_id
		self.owner = owner
		self.entity_type = entity_type
		self.cyborgCount = cyborgCount
		self.factoryProduction = factoryProduction
		self.fromFactory = fromFactory
		self.toFactory = toFactory
		self.troopSize = troopSize
		self.distanceToTarget = distanceToTarget

	def __str__(self):
		return "ID: %i, Type: %s" % (self.entity_id, self.entity_type)

def buildFactoryDict():
	rtn = {0: [], 1: [], -1: []}

	for e in entityObjects:
		if e.entity_type == "FACTORY":
			rtn[e.owner].append(e)

	return rtn

def captureGameInput():
	global entityObjects
	entity_count = int(input())  # the number of entities (e.g. factories and troops)
	for i in range(entity_count):
		entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
		entity_id = int(entity_id)
		owner = int(arg_1)
		if entity_type == "FACTORY":
			cyborgCount = int(arg_2)
			factoryProduction = int(arg_3)
			arg_4 = int(arg_4)
			arg_5 = int(arg_5)
			entityObjects.append(Entity(entity_id, owner, entity_type, cyborgCount, factoryProduction))
		else:
			fromFactory = int(arg_2)
			toFactory = int(arg_3)
			troopSize = int(arg_4)
			distanceToTarget = int(arg_5)
			entityObjects.append(Entity(entity_id, owner, entity_type, fromFactory=fromFactory, toFactory=toFactory, troopSize=troopSize, distanceToTarget=distanceToTarget))

def detFactoryToAttack():
	rtn = factoryDict[-1][0]
	score = rtn.cyborgCount
	for factory in factoryDict[-1][1:]:
		if factory.cyborgCount < score:
			score = factory.cyborgCount
			rtn = factory

	return rtn

def detFactoryToDefend():
	rtn = factoryDict[1][0]
	score = rtn.cyborgCount
	for factory in factoryDict[1][1:]:
		if factory.cyborgCount < score:
			score = factory.cyborgCount
			rtn = factory

	return rtn

def detClosestFriendlyFactoryTo(f2):
	rtn = factoryDict[1][0]
	dist = detDistance(rtn.entity_id, f2)
	for factory in factoryDict[1][1:]:
		if detDistance(factory.entity_id, f2) < dist:
			dist = detDistance(factory.entity_id, f2)
			rtn = factory
	print("Friendly: %i is closest to %i with a distance of %i" % (rtn.entity_id, f2, dist), file=sys.stderr)
	return rtn

def detDistance(f1, f2):
	try:
		return linkDict["%i|%i" % (min(int(f1), int(f2)), max(int(f1), int(f2)))]
	except(KeyError):
		return 99999

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories

neutralTroopPercent = 1.2
attackTroopPercent = 1.2
defendTroopPercent = 1.2

alwaysHoldingPercent = 0.4

#If above that percent, check next action, if percent below that action threshold, do that action
#Meaning all of these are currently set at 33% / 33% / 33%
attackPercent = 33
defendPercent = 66
waitPercent = 100

#NOTE: factory_1 < factory_2 
linkDict = {}
for i in range(link_count):
	factory_1, factory_2, distance = [int(j) for j in input().split()]
	linkDict[str(factory_1)+"|"+str(factory_2)] = distance

# game loop
while True:
	entityObjects = []
	captureGameInput()

	action = "WAIT"
	source = -1
	destination = -1
	cyborgs = 999999999

	factoryDict = buildFactoryDict()
	#If any factories are neutral
	if len(factoryDict[0]) > 0:
		print("Building up...", file=sys.stderr)
		#Have closest of your factories send 120% of minimum to that factory
		bestFromFactory = ""
		bestTo = -1
		smallestDist = 999999
		neutralCount = -1
		for neutralFactory in factoryDict[0]:
			nFID = neutralFactory.entity_id
			for factory in factoryDict[1]:
				if detDistance(nFID, factory.entity_id) < smallestDist:
					bestFromFactory = factory
					bestTo = nFID
					neutralCount = neutralFactory.cyborgCount
					smallestDist = detDistance(nFID, factory.entity_id)

		action = "MOVE"
		source = bestFromFactory.entity_id
		destination = bestTo
		print("%i*%.2f v. %i*%.2f" % (neutralCount, neutralTroopPercent, bestFromFactory.cyborgCount, alwaysHoldingPercent), file=sys.stderr)
		cyborgs = int(max(neutralCount*neutralTroopPercent, bestFromFactory.cyborgCount*alwaysHoldingPercent))


	else:
		acitonValue = r.randint(1,100)
		#Attack: Find weakest/closest enemy factory, Send 120% of minimum to that factory 
		if acitonValue < attackPercent:
			print("Attacking", file=sys.stderr)
			factoryToAttack = detFactoryToAttack()
			print("Going to attack %i" % (factoryToAttack.entity_id), file=sys.stderr)
			bestFromFactory = detClosestFriendlyFactoryTo(factoryToAttack.entity_id)
			action = "MOVE"
			source = bestFromFactory.entity_id
			destination = factoryToAttack.entity_id
			cyborgs = int(max(factoryToAttack.cyborgCount*attackTroopPercent, bestFromFactory.cyborgCount*alwaysHoldingPercent))
		#Defend: Find weakest friendly factory (or one being targeted), Send 120% of minimum to that factory
		elif acitonValue < defendPercent:
			print("Defending", file=sys.stderr)
			factoryToDefend = detFactoryToDefend()
			print("Going to defend %i" % (factoryToDefend.entity_id), file=sys.stderr)
			bestFromFactory = detClosestFriendlyFactoryTo(factoryToDefend.entity_id)
			action = "MOVE"
			source = bestFromFactory.entity_id
			destination = factoryToDefend.entity_id
			cyborgs = int(max(factoryToDefend.cyborgCount*defendTroopPercent, bestFromFactory.cyborgCount*alwaysHoldingPercent))
		#Neutral: Wait...
		else:
			print("Waiting", file=sys.stderr)
			pass

	print("Committing action", file=sys.stderr)
	# Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
	if action == "WAIT":
		print("WAIT")
	else:
		print("%s %i %i %i" % (action, source, destination, cyborgs))
